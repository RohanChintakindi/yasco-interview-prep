"""
=====================================================
 CHAPTER 4: TOOL-CALLING AGENTS
=====================================================

WHAT IS AN AGENT?
-----------------
A chain follows a fixed path: A -> B -> C. Always the same.
An AGENT decides what to do at each step. It's an LLM that can:

  1. Think about what to do
  2. Choose a TOOL to use (search, calculate, look up data, etc.)
  3. See the tool's result
  4. Decide: use another tool, or give the final answer?

This is a LOOP:
  Think -> Use Tool -> See Result -> Think -> Use Tool -> ... -> Answer

The LLM is in the driver's seat. It decides WHICH tools to use and
WHEN to stop. This is incredibly powerful.


WHAT ARE TOOLS?
---------------
A tool is any Python function that the LLM can call.
You describe what the tool does, and the LLM decides when to use it.

Examples:
  - search("query")       -> search the web
  - calculate("2 + 2")    -> do math
  - get_weather("Tokyo")  -> check weather API
  - read_file("data.csv") -> read a file

The LLM doesn't run the function directly. It says "I want to call
search('LangGraph tutorial')" and LangGraph actually runs it.


THE AGENT LOOP (ReAct Pattern):
  1. LLM sees the question + available tools
  2. LLM decides: "I should use the search tool"
  3. LangGraph runs the search tool
  4. Result goes back to the LLM
  5. LLM decides: "I have enough info, here's my answer"
  6. Done!

  Or step 5 might be: "I need more info, let me use another tool"
  And we loop back to step 3.


INSTALL:
  pip install langgraph langchain-openai python-dotenv


HOW TO RUN:
  python ch4_tool_calling_agents.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0,
)


# =============================================================================
# PART 1: CREATING TOOLS
# =============================================================================
#
# A tool is a Python function with the @tool decorator.
# The DOCSTRING is critical - the LLM reads it to understand what the tool does.
# Good docstrings = LLM picks the right tool. Bad docstrings = chaos.

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together. Use this for addition."""
    return a + b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together. Use this for multiplication."""
    return a * b


@tool
def get_word_length(word: str) -> int:
    """Get the length of a word (number of characters)."""
    return len(word)


@tool
def search_knowledge(query: str) -> str:
    """
    Search a knowledge base for information.
    Use this when you need facts or information about a topic.
    """
    # In a real app, this would search a database or the web.
    # Here we fake it with a simple dict.
    knowledge = {
        "python": "Python is a programming language created by Guido van Rossum in 1991.",
        "langgraph": "LangGraph is a library for building stateful AI agent workflows as graphs.",
        "langchain": "LangChain is a framework for building LLM applications, created by Harrison Chase.",
        "flask": "Flask is a lightweight Python web framework created by Armin Ronacher.",
    }

    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    return f"No information found for: {query}"


# Let's see what a tool looks like to the LLM:
print("=" * 60)
print("PART 1: Tools")
print("=" * 60)
print(f"Tool name: {add.name}")
print(f"Tool description: {add.description}")
print(f"Tool args: {add.args}")
print()


# =============================================================================
# PART 2: create_react_agent - THE EASY WAY
# =============================================================================
#
# LangGraph provides create_react_agent() which builds a complete
# agent graph for you. It implements the ReAct pattern:
#
#   [LLM thinks] -> [Call tool?] -> Yes -> [Run tool] -> [Back to LLM]
#                                -> No  -> [Return answer]
#
# You just give it an LLM and a list of tools. Done.

print("=" * 60)
print("PART 2: create_react_agent - Ready-made agent")
print("=" * 60)

# Create the agent with our tools
tools = [add, multiply, get_word_length, search_knowledge]
agent = create_react_agent(llm, tools)

# The agent is a compiled graph (a Runnable!)
# Input is a dict with "messages" key (it uses MessagesState)

# Let's ask it a math question:
print("--- Math question ---")
result = agent.invoke({
    "messages": [HumanMessage(content="What is 25 multiplied by 4, then add 13?")]
})

# The last message is the final answer
for msg in result["messages"]:
    print(f"  [{msg.type}]: {msg.content[:100]}")
print()

# What happened:
#   1. LLM saw the question and available tools
#   2. LLM decided: "I'll use multiply(25, 4)"
#   3. LangGraph ran multiply(25, 4) -> 100
#   4. LLM saw 100, decided: "Now I'll use add(100, 13)"
#   5. LangGraph ran add(100, 13) -> 113
#   6. LLM: "The answer is 113"


# =============================================================================
# PART 3: AGENT WITH KNOWLEDGE SEARCH
# =============================================================================

print("=" * 60)
print("PART 3: Agent searching for knowledge")
print("=" * 60)

result = agent.invoke({
    "messages": [HumanMessage(content="What is LangGraph and who created LangChain?")]
})

# Print the full conversation to see the agent's reasoning
for msg in result["messages"]:
    if msg.content:
        label = msg.type.upper()
        print(f"  [{label}]: {msg.content[:120]}")
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"  [TOOL CALL]: {tc['name']}({tc['args']})")
print()


# =============================================================================
# PART 4: STREAMING AGENT EXECUTION
# =============================================================================
#
# For a real chatbot, you want to see what the agent is doing in real time.
# .stream() shows each step as it happens.

print("=" * 60)
print("PART 4: Streaming agent steps")
print("=" * 60)

print("Question: How long is the word 'LangGraph'?\n")

for step in agent.stream({
    "messages": [HumanMessage(content="How long is the word 'LangGraph'? Tell me the exact count.")]
}):
    # Each step is {node_name: state_update}
    for node_name, update in step.items():
        if node_name == "__end__":
            continue
        print(f"  [{node_name}]")
        if "messages" in update:
            for msg in update["messages"]:
                if msg.content:
                    print(f"    {msg.content[:100]}")
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        print(f"    -> Calling {tc['name']}({tc['args']})")
print()


# =============================================================================
# PART 5: AGENT WITH SYSTEM PROMPT
# =============================================================================
#
# You can customize the agent's behavior with a system prompt.

print("=" * 60)
print("PART 5: Agent with custom system prompt")
print("=" * 60)

agent_with_personality = create_react_agent(
    llm,
    tools,
    prompt="You are a helpful but very concise assistant. "
           "Always use tools when available instead of guessing. "
           "Keep your final answer to 1-2 sentences maximum.",
)

result = agent_with_personality.invoke({
    "messages": [HumanMessage(content="What is Python? Also what's 7 times 8?")]
})

final_answer = result["messages"][-1].content
print(f"  Answer: {final_answer}")
print()


# =============================================================================
# PART 6: HOW THE AGENT GRAPH WORKS INTERNALLY
# =============================================================================
#
# create_react_agent builds this graph:
#
#   [START]
#      |
#      v
#   [agent] ──────────────────────────> [END]
#      |        (no tool calls?             ^
#      |         return answer)             |
#      v                                    |
#   [tools] ────────────────────────────────┘
#      |        (tool results go            |
#      └────> [agent]  (loop back!)
#
# Two nodes:
#   "agent":  Calls the LLM. LLM either returns tool calls or a final answer.
#   "tools":  Runs whatever tools the LLM requested.
#
# Conditional edge after "agent":
#   - If LLM made tool calls -> go to "tools"
#   - If LLM gave final answer -> go to END
#
# Edge after "tools":
#   - Always go back to "agent" (the LLM needs to see tool results)
#
# This is the ReAct loop. "Reason" (agent) + "Act" (tools), repeat.


# =============================================================================
# PART 7: WHEN TO USE AGENTS VS CHAINS
# =============================================================================
#
# USE A CHAIN (LangChain) WHEN:
#   - The steps are always the same
#   - No decisions needed
#   - Simple: input -> process -> output
#   - Example: RAG (retrieve -> prompt -> generate)
#
# USE AN AGENT (LangGraph) WHEN:
#   - The LLM needs to DECIDE what to do
#   - Multiple tools might be needed
#   - The number of steps isn't known in advance
#   - Example: "Research this topic" (might need 1 search or 5)
#
# USE A CUSTOM GRAPH (LangGraph) WHEN:
#   - You need specific control over the workflow
#   - Multi-agent collaboration
#   - Human-in-the-loop approval steps
#   - Complex branching logic


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Create a tool:
#   @tool
#   def my_tool(arg: str) -> str:
#       """Description the LLM reads."""  # <- IMPORTANT!
#       return result
#
# Create agent (easy way):
#   agent = create_react_agent(llm, [tool1, tool2])
#
# Run agent:
#   result = agent.invoke({"messages": [HumanMessage(content="...")]})
#   answer = result["messages"][-1].content
#
# Stream agent:
#   for step in agent.stream({"messages": [...]}):
#       print(step)
#
# =============================================================================
