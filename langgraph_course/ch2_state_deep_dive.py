"""
=====================================================
 CHAPTER 2: STATE - THE HEART OF LANGGRAPH
=====================================================

WHY STATE MATTERS
-----------------
In LangChain chains, data flows forward and that's it.
In LangGraph, STATE is the shared memory that every node reads and writes.

Think of it like a shared Google Doc:
  - Node A opens the doc, writes some info, closes it
  - Node B opens the doc, reads what A wrote, adds more, closes it
  - Node C opens the doc, reads everything, makes final edits

The "Google Doc" is your state. It's the SINGLE SOURCE OF TRUTH
for your entire workflow.


THE MOST IMPORTANT CONCEPT: REDUCERS
--------------------------------------
When a node returns {"messages": new_message}, what happens to
the existing messages in state?

  Option A: REPLACE - new value overwrites old value
  Option B: APPEND  - new value is ADDED to old value

This is controlled by REDUCERS. A reducer is a function that decides
how to MERGE a node's output into the existing state.

  Default (no reducer): REPLACE. New value overwrites old.
  With Annotated[list, operator.add]: APPEND. New items are added to the list.

This is crucial for chat apps: you want messages to ACCUMULATE,
not get overwritten each turn.


INSTALL:
  pip install langgraph langchain-openai python-dotenv


HOW TO RUN:
  python ch2_state_deep_dive.py
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator


# =============================================================================
# PART 1: DEFAULT BEHAVIOR - REPLACE
# =============================================================================
#
# Without a reducer, returning a key OVERWRITES the previous value.

print("=" * 60)
print("PART 1: Default behavior - Replace")
print("=" * 60)


class ReplaceState(TypedDict):
    value: str


def step_a(state: ReplaceState) -> dict:
    print(f"  Step A sees: '{state.get('value', '')}'")
    return {"value": "Hello from A"}


def step_b(state: ReplaceState) -> dict:
    print(f"  Step B sees: '{state['value']}'")
    return {"value": "Hello from B"}  # This REPLACES A's value!


graph = StateGraph(ReplaceState)
graph.add_node("a", step_a)
graph.add_node("b", step_b)
graph.add_edge(START, "a")
graph.add_edge("a", "b")
graph.add_edge("b", END)
app = graph.compile()

result = app.invoke({"value": "initial"})
print(f"  Final value: '{result['value']}'")
print()

# Result: "Hello from B" - Step B's value REPLACED Step A's value.
# This is the DEFAULT. Each node's return OVERWRITES the state key.


# =============================================================================
# PART 2: APPEND REDUCER - ACCUMULATE VALUES
# =============================================================================
#
# For lists (like chat messages), you usually want to APPEND, not replace.
# Use Annotated[list, operator.add] to tell LangGraph:
#   "When a node returns items for this key, ADD them to the existing list."
#
# operator.add for lists does: existing_list + new_list = combined_list
#   [1, 2] + [3] = [1, 2, 3]

print("=" * 60)
print("PART 2: Append reducer - Accumulating values")
print("=" * 60)


class AppendState(TypedDict):
    # Annotated[list, operator.add] means:
    # "This is a list, and new values should be APPENDED, not replaced"
    messages: Annotated[list, operator.add]
    final_count: int  # No reducer = replace behavior


def add_greeting(state: AppendState) -> dict:
    # Return a LIST - it will be APPENDED to state["messages"]
    return {"messages": ["Hello!"]}


def add_question(state: AppendState) -> dict:
    return {"messages": ["How are you?"]}


def add_farewell(state: AppendState) -> dict:
    count = len(state["messages"]) + 1  # +1 for the one we're adding
    return {
        "messages": ["Goodbye!"],
        "final_count": count,  # This REPLACES (no reducer)
    }


graph = StateGraph(AppendState)
graph.add_node("greeting", add_greeting)
graph.add_node("question", add_question)
graph.add_node("farewell", add_farewell)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "question")
graph.add_edge("question", "farewell")
graph.add_edge("farewell", END)
app = graph.compile()

result = app.invoke({"messages": []})
print(f"  Messages: {result['messages']}")
print(f"  Count: {result['final_count']}")
print()

# Result: ["Hello!", "How are you?", "Goodbye!"]
# Each node APPENDED its message. Nothing was lost!
#
# Without the reducer, each node would REPLACE the list:
# After greeting: ["Hello!"]
# After question: ["How are you?"]  <- "Hello!" would be GONE
# After farewell: ["Goodbye!"]       <- everything gone except last


# =============================================================================
# PART 3: WHY THIS MATTERS - CHAT MESSAGE ACCUMULATION
# =============================================================================
#
# This is THE pattern for chatbots and agents in LangGraph.
# Every turn adds messages to the list. The full history is preserved.
#
# LangGraph provides a built-in MessagesState for this exact use case.

print("=" * 60)
print("PART 3: MessagesState - The built-in chat state")
print("=" * 60)

from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# MessagesState is a TypedDict with ONE key:
#   messages: Annotated[list[BaseMessage], add_messages]
#
# add_messages is a smart reducer that:
#   - Appends new messages to the list
#   - Can update existing messages by ID
#   - Handles message deduplication
#
# This is the state you'll use 90% of the time for chat/agent workflows.


def chatbot_node(state: MessagesState) -> dict:
    """A node that reads messages and adds a response."""
    last_message = state["messages"][-1]
    response = f"You said: '{last_message.content}'. That's interesting!"
    return {"messages": [AIMessage(content=response)]}


graph = StateGraph(MessagesState)
graph.add_node("bot", chatbot_node)
graph.add_edge(START, "bot")
graph.add_edge("bot", END)
app = graph.compile()

# Start with a human message
result = app.invoke({
    "messages": [HumanMessage(content="I love Python")]
})

print("Conversation:")
for msg in result["messages"]:
    role = "Human" if isinstance(msg, HumanMessage) else "AI"
    print(f"  {role}: {msg.content}")
print()


# =============================================================================
# PART 4: CUSTOM STATE WITH MULTIPLE FIELDS
# =============================================================================
#
# Real apps need more than just messages. You might track:
#   - The current step in a workflow
#   - A counter (how many times we've looped)
#   - Retrieved documents
#   - Whether human approval was given
#   - Error messages

print("=" * 60)
print("PART 4: Custom state with multiple fields")
print("=" * 60)


class ResearchState(TypedDict):
    topic: str                                     # What we're researching (replace)
    messages: Annotated[list, operator.add]         # Chat history (append)
    sources: Annotated[list[str], operator.add]     # Found sources (append)
    iteration: int                                  # Current iteration (replace)
    is_complete: bool                               # Done flag (replace)


def research(state: ResearchState) -> dict:
    topic = state["topic"]
    iteration = state.get("iteration", 0) + 1
    return {
        "messages": [f"Researching '{topic}' (iteration {iteration})"],
        "sources": [f"https://example.com/{topic}/{iteration}"],
        "iteration": iteration,
    }


def evaluate(state: ResearchState) -> dict:
    enough = state["iteration"] >= 2  # Done after 2 iterations
    return {
        "messages": [f"Evaluation: {'complete' if enough else 'need more'}"],
        "is_complete": enough,
    }


graph = StateGraph(ResearchState)
graph.add_node("research", research)
graph.add_node("evaluate", evaluate)
graph.add_edge(START, "research")
graph.add_edge("research", "evaluate")

# CONDITIONAL EDGE: if not complete, go back to research (a LOOP!)
# We'll cover this properly in Chapter 3, but here's a preview:
graph.add_conditional_edges(
    "evaluate",
    lambda state: END if state["is_complete"] else "research",
)

app = graph.compile()

result = app.invoke({
    "topic": "langgraph",
    "messages": [],
    "sources": [],
    "iteration": 0,
    "is_complete": False,
})

print(f"Messages: {result['messages']}")
print(f"Sources: {result['sources']}")
print(f"Iterations: {result['iteration']}")
print(f"Complete: {result['is_complete']}")
print()

# The graph LOOPED: research -> evaluate -> research -> evaluate -> END
# Messages and sources ACCUMULATED across iterations.
# iteration was REPLACED each time (no reducer).


# =============================================================================
# PART 5: STATE DESIGN PRINCIPLES
# =============================================================================
#
# 1. USE APPEND (Annotated[list, operator.add]) FOR:
#    - Chat messages (always accumulate)
#    - Logs/history (track what happened)
#    - Collected items (search results, sources)
#
# 2. USE REPLACE (default) FOR:
#    - Counters (iteration = 3, not [1, 2, 3])
#    - Flags (is_complete = True)
#    - Current values (current_topic = "AI")
#    - Single objects (final_answer = "...")
#
# 3. KEEP STATE MINIMAL:
#    Don't put everything in state. Only put data that
#    NEEDS to be shared between nodes.
#
# 4. USE MessagesState WHEN POSSIBLE:
#    For chat/agent workflows, MessagesState is the standard.
#    Add extra fields by extending it:
#
#    class MyState(MessagesState):
#        topic: str
#        iteration: int


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Basic state (replace behavior):
#   class MyState(TypedDict):
#       value: str          # New value replaces old
#       count: int          # New value replaces old
#
# State with append:
#   class MyState(TypedDict):
#       items: Annotated[list, operator.add]  # New items appended
#
# Built-in chat state:
#   from langgraph.graph import MessagesState
#   # Has messages: list with smart append reducer
#
# Extended chat state:
#   class MyState(MessagesState):
#       extra_field: str
#
# Node function signature:
#   def my_node(state: MyState) -> dict:
#       return {"key": new_value}  # Only return what changed
#
# =============================================================================
