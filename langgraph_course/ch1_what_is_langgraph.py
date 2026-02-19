"""
==============================================
 CHAPTER 1: WHAT IS LANGGRAPH & WHY DO YOU NEED IT?
==============================================

PREREQUISITES
-------------
You should understand LangChain basics first (LLMs, prompts, chains, LCEL).
If not, go through the langchain_course folder first.


THE PROBLEM WITH LANGCHAIN CHAINS
----------------------------------
In LangChain, a chain is LINEAR:

  Input -> Step A -> Step B -> Step C -> Output

Data flows in one direction, left to right. That's great for:
  - "Take a question, retrieve docs, generate answer" (RAG)
  - "Take input, format prompt, call LLM, parse output"

But real AI applications need MORE:

  - LOOPS: "If the answer is bad, go back and try again"
  - BRANCHING: "If the user wants X, do this. If Y, do that."
  - HUMAN-IN-THE-LOOP: "Pause here, let a human review, then continue"
  - MULTI-AGENT: "Agent A does research, Agent B writes, Agent C reviews"

You CAN'T do loops or conditional branching with a simple chain.
prompt | llm | parser always goes forward. It never goes back.


WHAT IS LANGGRAPH?
------------------
LangGraph lets you build AI workflows as GRAPHS instead of chains.

A graph has:
  - NODES: Steps that do work (call an LLM, run a tool, process data)
  - EDGES: Connections between nodes (which step goes next)
  - STATE: Data that flows through the graph and gets updated at each step

The key difference from chains:

  CHAIN (LangChain):
    A -> B -> C -> Done
    (always the same path, always forward)

  GRAPH (LangGraph):
    A -> B -> C
         ^    |
         |    v
         +-- D (if condition, go back to B)
    (can loop, branch, and make decisions)

Think of it like this:
  - A CHAIN is a conveyor belt: items move forward, one step at a time
  - A GRAPH is a flowchart: items can branch, loop, and take different paths


REAL EXAMPLES WHERE YOU NEED LANGGRAPH
---------------------------------------
1. SELF-CORRECTING AGENT:
   Generate code -> Run it -> If error, go back and fix -> Run again -> Done
   (This is a LOOP - impossible with a chain)

2. MULTI-STEP RESEARCH:
   Search web -> Read results -> Need more info? -> Search again -> Summarize
   (Loop until you have enough information)

3. APPROVAL WORKFLOW:
   Draft email -> Human reviews -> Approved? Send it : Revise and try again
   (Human-in-the-loop with conditional branching)

4. MULTI-AGENT SYSTEM:
   Researcher finds info -> Writer drafts -> Reviewer critiques -> Writer revises
   (Multiple agents collaborating in a cycle)


THE CORE CONCEPTS (WE'LL LEARN EACH IN DETAIL)
-----------------------------------------------
1. STATE:   A dict-like object that holds all the data flowing through the graph
2. NODES:   Functions that read state, do work, and update state
3. EDGES:   Connections between nodes (can be conditional)
4. GRAPH:   The full workflow (nodes + edges + state)


INSTALL:
  pip install langgraph langchain-openai python-dotenv


HOW TO RUN THIS FILE:
  python ch1_what_is_langgraph.py
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict


# =============================================================================
# PART 1: STATE - THE DATA THAT FLOWS THROUGH YOUR GRAPH
# =============================================================================
#
# State is a TypedDict (a dict with typed keys) that holds ALL the data
# your workflow needs. Every node can read and update the state.
#
# Think of state like a clipboard being passed around an office:
#   - Person A writes "topic: AI" on the clipboard, passes it to Person B
#   - Person B reads the topic, writes "research: [AI article]", passes to C
#   - Person C reads the research, writes "summary: ...", passes to D
#
# The clipboard IS the state. Everyone reads from it and writes to it.

class SimpleState(TypedDict):
    """
    This defines WHAT data our graph carries around.
    Every key is a piece of data that nodes can read/update.
    """
    name: str       # A person's name
    greeting: str   # The greeting we generate


# =============================================================================
# PART 2: NODES - FUNCTIONS THAT DO WORK
# =============================================================================
#
# A node is just a Python function that:
#   1. Receives the current state (dict)
#   2. Does some work
#   3. Returns a dict of state UPDATES (what changed)
#
# IMPORTANT: Nodes return ONLY the keys they want to UPDATE.
# You don't need to return the entire state - just the changes.

def greet(state: SimpleState) -> dict:
    """
    Node that creates a greeting from the name.
    Reads state["name"], produces state["greeting"].
    """
    name = state["name"]
    return {"greeting": f"Hello, {name}! Welcome to LangGraph!"}


def shout(state: SimpleState) -> dict:
    """
    Node that uppercases the greeting.
    Reads state["greeting"], updates state["greeting"].
    """
    return {"greeting": state["greeting"].upper()}


# =============================================================================
# PART 3: BUILDING YOUR FIRST GRAPH
# =============================================================================
#
# A StateGraph is built in 3 steps:
#   1. Add nodes (the steps)
#   2. Add edges (the connections between steps)
#   3. Compile (turns it into a runnable)
#
# Every graph has two special nodes:
#   START -> where execution begins
#   END   -> where execution stops

print("=" * 60)
print("PART 3: Your first graph")
print("=" * 60)

# Step 1: Create a graph with our state type
graph = StateGraph(SimpleState)

# Step 2: Add nodes
# The first argument is the node's NAME (a string)
# The second argument is the FUNCTION to run
graph.add_node("greet", greet)
graph.add_node("shout", shout)

# Step 3: Add edges (connections)
# START -> greet -> shout -> END
graph.add_edge(START, "greet")  # Start by running the greet node
graph.add_edge("greet", "shout")  # After greet, run shout
graph.add_edge("shout", END)  # After shout, we're done

# Step 4: Compile the graph into a runnable
# After compiling, the graph works just like any LangChain Runnable:
# it has .invoke(), .stream(), etc.
app = graph.compile()

# Step 5: Run it!
result = app.invoke({"name": "Chint"})

print(f"Input:  name = 'Chint'")
print(f"Output: {result}")
print(f"Greeting: {result['greeting']}")
print()

# What happened:
#   1. We passed {"name": "Chint"} as the initial state
#   2. START -> "greet" node ran: read "Chint", produced "Hello, Chint!..."
#   3. "greet" -> "shout" node ran: read greeting, uppercased it
#   4. "shout" -> END: execution finished
#   5. We got back the final state with all updates applied


# =============================================================================
# PART 4: TRACING EXECUTION STEP BY STEP
# =============================================================================
#
# .stream() on a graph doesn't stream text like an LLM.
# It streams STATE UPDATES after each node runs.
# This is great for debugging: you can see what each node did.

print("=" * 60)
print("PART 4: Streaming state updates (debugging)")
print("=" * 60)

for step in app.stream({"name": "Alice"}):
    # Each step is a dict: {node_name: state_updates}
    print(f"Step: {step}")

print()

# Output will look like:
#   Step: {'greet': {'greeting': 'Hello, Alice! Welcome to LangGraph!'}}
#   Step: {'shout': {'greeting': 'HELLO, ALICE! WELCOME TO LANGGRAPH!'}}
#
# You can see exactly what each node produced.


# =============================================================================
# PART 5: GRAPH VISUALIZATION (MENTAL MODEL)
# =============================================================================
#
# Our graph looks like this:
#
#   [START]
#      |
#      v
#   [greet]  -- reads name, writes greeting
#      |
#      v
#   [shout]  -- reads greeting, uppercases it
#      |
#      v
#    [END]
#
# This is a simple LINEAR graph - exactly like a LangChain chain.
# "So why use LangGraph?" you ask.
#
# Because in Chapter 3, we'll add CONDITIONAL EDGES:
#   [shout] -> if too short, go back to [greet]
#           -> if good enough, go to [END]
#
# THAT'S the power of LangGraph: conditional flow and loops.
# But first, Chapter 2 covers state in more depth.


# =============================================================================
# PART 6: COMPILED GRAPH = RUNNABLE
# =============================================================================
#
# After .compile(), the graph is a Runnable. It has all the methods
# you learned in LangChain:
#
#   app.invoke(state)    -> Run the full graph, return final state
#   app.stream(state)    -> Stream state updates after each node
#   app.batch([states])  -> Run multiple inputs in parallel
#
# This means you can even use a LangGraph graph INSIDE a LangChain chain!
# It's all Runnables, all the way down.

print("=" * 60)
print("PART 6: Batch execution")
print("=" * 60)

results = app.batch([
    {"name": "Chint"},
    {"name": "Alice"},
    {"name": "Bob"},
])

for r in results:
    print(f"  {r['greeting']}")

print()


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
#
# 1. LangGraph builds AI workflows as GRAPHS (nodes + edges + state)
# 2. STATE: a TypedDict that holds all data flowing through the graph
# 3. NODES: functions that read state and return updates
# 4. EDGES: connections that define which node runs next
# 5. START and END are special nodes marking the beginning and end
# 6. .compile() turns the graph into a Runnable (invoke/stream/batch)
# 7. Graphs can do things chains CAN'T: loops, branches, conditionals
#
# Next: Chapter 2 dives deep into state management.
#
# =============================================================================
