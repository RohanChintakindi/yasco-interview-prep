"""
=====================================================
 CHAPTER 6: BUILDING A CUSTOM AGENT FROM SCRATCH
=====================================================

In Chapter 4, we used create_react_agent() - a pre-built agent.
Now let's build one MANUALLY to understand how agents work inside.

This is important because:
  1. You understand what's actually happening (no magic)
  2. You can customize every part of the workflow
  3. You can add nodes that pre-built agents don't have
     (human review, logging, multi-model routing, etc.)


THE AGENT LOOP (we're building this by hand):

  ┌──────────────────────────────────────────────┐
  │                                              │
  │   [agent]  LLM decides: use tool or answer?  │
  │      |                                       │
  │      ├── tool calls? ──> [tools] runs them ──┘
  │      |                    (loops back to agent)
  │      └── no tool calls? ──> [END]
  │
  └──────────────────────────────────────────────┘


INSTALL:
  pip install langgraph langchain-openai python-dotenv


HOW TO RUN:
  python ch6_building_a_custom_agent.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv

load_dotenv()


# =============================================================================
# STEP 1: DEFINE TOOLS
# =============================================================================

@tool
def search(query: str) -> str:
    """Search the web for information. Use for any factual questions."""
    # Fake search results
    results = {
        "weather paris": "Paris weather: 18°C, partly cloudy.",
        "population japan": "Japan has a population of approximately 125 million.",
        "capital australia": "The capital of Australia is Canberra.",
        "python creator": "Python was created by Guido van Rossum in 1991.",
    }
    for key, value in results.items():
        if key in query.lower():
            return value
    return f"Search results for '{query}': No specific results found. This is a demo."


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression. Example: '2 + 3 * 4'"""
    try:
        result = eval(expression)  # In production, use a safe math parser!
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {e}"


tools = [search, calculator]


# =============================================================================
# STEP 2: CREATE THE LLM WITH TOOL BINDING
# =============================================================================
#
# .bind_tools() tells the LLM what tools are available.
# The LLM doesn't RUN the tools - it generates "tool call" messages
# that describe WHICH tool to call and with WHAT arguments.
# LangGraph then actually runs the tools.

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0,
)

# Bind tools: now the LLM knows these tools exist
llm_with_tools = llm.bind_tools(tools)


# =============================================================================
# STEP 3: DEFINE THE AGENT NODE
# =============================================================================
#
# The agent node calls the LLM. The LLM either:
#   a) Returns tool calls (it wants to use a tool)
#   b) Returns a text response (it has the final answer)

def agent_node(state: MessagesState) -> dict:
    """
    Call the LLM with the conversation so far.
    The LLM decides: use a tool or give a final answer.
    """
    # Add a system message to guide the agent
    system = SystemMessage(
        content="You are a helpful assistant. Use tools when needed. "
                "Be concise in your final answers."
    )

    # Call the LLM with system prompt + all messages so far
    response = llm_with_tools.invoke([system] + state["messages"])

    # Return the LLM's response as a new message
    return {"messages": [response]}


# =============================================================================
# STEP 4: DEFINE THE TOOL NODE
# =============================================================================
#
# ToolNode is a pre-built node that:
#   1. Reads the LLM's tool call messages
#   2. Actually runs the requested tools
#   3. Returns tool result messages
#
# You CAN build this yourself, but ToolNode handles edge cases for you.

tool_node = ToolNode(tools)


# =============================================================================
# STEP 5: DEFINE THE ROUTING FUNCTION
# =============================================================================
#
# After the agent runs, we need to decide:
#   - Did the LLM make tool calls? -> Go to "tools" node
#   - Did the LLM give a final answer? -> Go to END

def should_use_tools(state: MessagesState) -> str:
    """
    Check the last message from the LLM.
    If it contains tool calls, route to the tools node.
    Otherwise, we're done.
    """
    last_message = state["messages"][-1]

    # tool_calls is a list of tool call requests from the LLM
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"   # LLM wants to use tools -> run them
    else:
        return END       # LLM gave a final answer -> done


# =============================================================================
# STEP 6: BUILD THE GRAPH
# =============================================================================
#
# Now we connect everything:
#
#   START -> agent -> should_use_tools? -> tools -> agent (loop)
#                                       -> END

print("=" * 60)
print("Building the custom agent graph")
print("=" * 60)

graph = StateGraph(MessagesState)

# Add nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

# Add edges
graph.add_edge(START, "agent")                      # Start with the agent
graph.add_conditional_edges("agent", should_use_tools)  # Agent decides: tools or done
graph.add_edge("tools", "agent")                    # After tools, back to agent

# Compile
app = graph.compile()

print("Graph built!\n")

# Visualize the graph structure:
#
#   [START]
#      |
#      v
#   [agent] ─── no tool calls ──> [END]
#      ^   |
#      |   └── has tool calls ──> [tools]
#      |                             |
#      └─────────────────────────────┘


# =============================================================================
# STEP 7: TEST THE AGENT
# =============================================================================

print("=" * 60)
print("Testing the custom agent")
print("=" * 60)

# Test 1: Simple question (no tools needed)
print("\n--- Test 1: Simple question ---")
result = app.invoke({"messages": [HumanMessage(content="What is 2 + 2?")]})
print(f"  Answer: {result['messages'][-1].content}")

# Test 2: Needs search tool
print("\n--- Test 2: Needs search ---")
result = app.invoke({
    "messages": [HumanMessage(content="What's the weather like in Paris?")]
})
print(f"  Answer: {result['messages'][-1].content}")

# Test 3: Needs calculator
print("\n--- Test 3: Needs calculator ---")
result = app.invoke({
    "messages": [HumanMessage(content="Calculate 156 * 23 + 89")]
})
print(f"  Answer: {result['messages'][-1].content}")

# Test 4: Multiple tools needed
print("\n--- Test 4: Multiple tools ---")
result = app.invoke({
    "messages": [HumanMessage(
        content="Who created Python? Also, what is 2024 minus the year Python was created?"
    )]
})
print(f"  Answer: {result['messages'][-1].content}")
print()


# =============================================================================
# STEP 8: STREAMING THE AGENT'S THOUGHT PROCESS
# =============================================================================

print("=" * 60)
print("Streaming agent execution")
print("=" * 60)

print("\nQuestion: What is the population of Japan? Divide it by 1000.\n")

for step in app.stream({
    "messages": [HumanMessage(
        content="What is the population of Japan? Divide that number by 1000."
    )]
}):
    for node_name, update in step.items():
        if node_name == "__end__":
            continue
        print(f"[{node_name}]")
        for msg in update.get("messages", []):
            if msg.content:
                print(f"  Content: {msg.content[:100]}")
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"  Tool call: {tc['name']}({tc['args']})")
        print()


# =============================================================================
# WHY BUILD CUSTOM vs create_react_agent?
# =============================================================================
#
# create_react_agent is GREAT for simple tool-using agents.
# Build CUSTOM when you need:
#
# 1. EXTRA NODES:
#    agent -> tools -> VALIDATOR -> agent
#    (validate tool results before showing to LLM)
#
# 2. HUMAN APPROVAL:
#    agent -> tools -> HUMAN_REVIEW -> agent
#    (pause for human to approve tool usage)
#
# 3. MULTIPLE AGENTS:
#    researcher -> writer -> reviewer -> writer (loop)
#    (different LLMs or prompts for each role)
#
# 4. CUSTOM ROUTING:
#    agent -> if tool is "dangerous" -> human_review
#          -> if tool is "safe" -> tools
#    (different handling based on which tool)
#
# 5. LOGGING/MONITORING:
#    agent -> LOGGER -> tools -> LOGGER -> agent
#    (track every step for debugging)


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Bind tools to LLM:
#   llm_with_tools = llm.bind_tools([tool1, tool2])
#
# Agent node:
#   def agent(state: MessagesState) -> dict:
#       response = llm_with_tools.invoke(state["messages"])
#       return {"messages": [response]}
#
# Tool node (pre-built):
#   from langgraph.prebuilt import ToolNode
#   tool_node = ToolNode([tool1, tool2])
#
# Routing function:
#   def route(state):
#       if state["messages"][-1].tool_calls:
#           return "tools"
#       return END
#
# Graph:
#   graph.add_node("agent", agent_fn)
#   graph.add_node("tools", tool_node)
#   graph.add_edge(START, "agent")
#   graph.add_conditional_edges("agent", route_fn)
#   graph.add_edge("tools", "agent")
#
# =============================================================================
