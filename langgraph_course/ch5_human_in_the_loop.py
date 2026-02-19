"""
=====================================================
 CHAPTER 5: HUMAN-IN-THE-LOOP & CHECKPOINTS
=====================================================

THE PROBLEM
-----------
Sometimes you don't want AI to act fully autonomously:
  - An agent wants to send an email. Should it just send it? Or ask you first?
  - An agent wants to delete files. Shouldn't a human approve that?
  - An agent drafted a report. A manager should review before publishing.

HUMAN-IN-THE-LOOP means: pause the graph, let a human review/modify,
then resume execution.


CHECKPOINTS
-----------
For human-in-the-loop to work, LangGraph needs to SAVE the graph's state
so it can be resumed later. This is called a CHECKPOINT.

A checkpoint is a snapshot of the state at a specific point in execution.
LangGraph saves these using a "checkpointer" (a storage backend).

  MemorySaver:        Saves in memory (for testing, lost on restart)
  SqliteSaver:        Saves to SQLite database (persistent)
  PostgresSaver:      Saves to Postgres (production)


THE interrupt() PATTERN
-----------------------
LangGraph provides interrupt() - when a node calls this function,
the graph PAUSES. The caller gets back the state so far. A human
can review it, optionally modify it, and then resume the graph
with a Command.

  Graph starts -> Node A runs -> Node B calls interrupt("Please review")
  -> PAUSED. Human sees the state.
  -> Human says "approved" (sends a Command to resume)
  -> Graph resumes from where it paused -> Node C runs -> Done


INSTALL:
  pip install langgraph langchain-openai python-dotenv


HOW TO RUN:
  python ch5_human_in_the_loop.py
"""

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0.2,
)


# =============================================================================
# PART 1: BASIC INTERRUPT - PAUSE AND RESUME
# =============================================================================
#
# interrupt() pauses the graph and returns a value to the caller.
# When the graph is resumed, interrupt() returns the human's input.

print("=" * 60)
print("PART 1: Basic interrupt - Pause and resume")
print("=" * 60)

from typing import TypedDict


class ApprovalState(TypedDict):
    request: str
    draft: str
    approved: bool
    final: str


def write_draft(state: ApprovalState) -> dict:
    """AI writes a draft response."""
    prompt = ChatPromptTemplate.from_template(
        "Write a short, professional email response to: {request}\n"
        "Keep it to 2-3 sentences."
    )
    chain = prompt | llm | StrOutputParser()
    draft = chain.invoke({"request": state["request"]})
    print(f"  [AI Draft]: {draft}")
    return {"draft": draft}


def human_review(state: ApprovalState) -> dict:
    """Pause for human review using interrupt()."""
    # interrupt() PAUSES the graph here.
    # The string is shown to the human as context.
    # When resumed, interrupt() returns the human's response.
    human_input = interrupt(
        f"Please review this draft:\n\n{state['draft']}\n\nType 'approve' or give feedback:"
    )

    if human_input.lower().strip() == "approve":
        return {"approved": True}
    else:
        return {"approved": False, "draft": human_input}  # Human provided revised text


def finalize(state: ApprovalState) -> dict:
    """Finalize the approved draft."""
    if state["approved"]:
        return {"final": f"SENT: {state['draft']}"}
    else:
        return {"final": f"REVISED AND SENT: {state['draft']}"}


# Build graph
graph = StateGraph(ApprovalState)
graph.add_node("write", write_draft)
graph.add_node("review", human_review)
graph.add_node("finalize", finalize)

graph.add_edge(START, "write")
graph.add_edge("write", "review")
graph.add_edge("review", "finalize")
graph.add_edge("finalize", END)

# IMPORTANT: To use interrupt(), you MUST provide a checkpointer.
# The checkpointer saves state so the graph can be resumed.
memory = MemorySaver()
app = graph.compile(checkpointer=memory)

# Run the graph - it will PAUSE at the interrupt
# thread_id groups related runs together (like a conversation)
config = {"configurable": {"thread_id": "email-1"}}

print("\nStarting graph (will pause at human review)...\n")
result = app.invoke(
    {"request": "Thank the client for their feedback", "draft": "", "approved": False, "final": ""},
    config=config,
)

# At this point, the graph is PAUSED at the interrupt.
# In a real app, you'd show the draft to a human in a UI.
# Here, we'll simulate the human approving:

print("\n[Human approves the draft]\n")

# Resume the graph with the human's input
result = app.invoke(
    Command(resume="approve"),  # This is what the human "types"
    config=config,
)

print(f"\n  Result: {result['final']}")
print()


# =============================================================================
# PART 2: UNDERSTANDING CHECKPOINTS & THREADS
# =============================================================================
#
# THREAD: A thread_id groups related graph runs together.
#   Think of it like a conversation ID. All messages in one chat
#   share the same thread_id.
#
# CHECKPOINT: A snapshot of state saved at each step.
#   LangGraph saves a checkpoint AFTER every node runs.
#   This means you can:
#     - Pause and resume (human-in-the-loop)
#     - Replay from any point (debugging)
#     - Continue a conversation later
#
# Different thread_ids = completely separate workflows.
# Same thread_id = continues the same workflow.

print("=" * 60)
print("PART 2: Threads - separate conversations")
print("=" * 60)

# Simple chatbot graph to demonstrate threads
def echo_bot(state: MessagesState) -> dict:
    last = state["messages"][-1].content
    return {"messages": [AIMessage(content=f"Echo: {last}")]}


graph = StateGraph(MessagesState)
graph.add_node("bot", echo_bot)
graph.add_edge(START, "bot")
graph.add_edge("bot", END)

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

# Thread 1: Alice's conversation
config_alice = {"configurable": {"thread_id": "alice-chat"}}
app.invoke({"messages": [HumanMessage(content="Hi I'm Alice")]}, config_alice)
result = app.invoke({"messages": [HumanMessage(content="What's my name?")]}, config_alice)
print(f"  Alice's thread: {[m.content for m in result['messages']]}")

# Thread 2: Bob's conversation (completely separate)
config_bob = {"configurable": {"thread_id": "bob-chat"}}
result = app.invoke({"messages": [HumanMessage(content="I'm Bob")]}, config_bob)
print(f"  Bob's thread: {[m.content for m in result['messages']]}")
print()

# Each thread has its own state. Alice's messages don't leak into Bob's.


# =============================================================================
# PART 3: VIEWING GRAPH STATE
# =============================================================================
#
# You can inspect the current state of any thread at any time.
# This is useful for debugging and for building UIs.

print("=" * 60)
print("PART 3: Inspecting graph state")
print("=" * 60)

state_snapshot = app.get_state(config_alice)
print(f"  Alice's current state:")
print(f"    Messages: {len(state_snapshot.values['messages'])}")
print(f"    Next node: {state_snapshot.next}")  # What would run next (empty if done)
print()


# =============================================================================
# PART 4: WHY THIS MATTERS IN REAL APPS
# =============================================================================
#
# HUMAN-IN-THE-LOOP USE CASES:
#
# 1. CONTENT MODERATION:
#    AI generates content -> Human reviews -> Approve/reject
#    Uses: interrupt() at the review step
#
# 2. TOOL APPROVAL:
#    Agent wants to call an API -> Pause -> "Agent wants to call
#    send_email(to='boss@company.com'). Allow?" -> Resume
#    Uses: interrupt() before executing sensitive tools
#
# 3. MULTI-STEP WORKFLOWS:
#    Draft -> Review -> Revise -> Review -> Approve -> Publish
#    Uses: loop with interrupt() at each review step
#
# 4. COLLABORATIVE AI:
#    AI proposes a plan -> Human modifies the plan -> AI executes
#    Uses: interrupt() after planning, resume with modified plan
#
#
# CHECKPOINT USE CASES:
#
# 1. LONG-RUNNING TASKS:
#    A research agent that runs for hours. If it crashes, you can
#    resume from the last checkpoint instead of starting over.
#
# 2. PERSISTENT CHATBOTS:
#    User chats, closes the app, comes back tomorrow. The conversation
#    continues from where they left off (saved in checkpoints).
#
# 3. DEBUGGING:
#    Something went wrong at step 5. Replay from step 4's checkpoint
#    with modified state to test a fix.


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Interrupt (pause for human):
#   from langgraph.types import interrupt, Command
#
#   def my_node(state):
#       human_input = interrupt("Review this: ...")
#       return {"approved": human_input == "yes"}
#
# Checkpointer (required for interrupt):
#   from langgraph.checkpoint.memory import MemorySaver
#   memory = MemorySaver()
#   app = graph.compile(checkpointer=memory)
#
# Thread config:
#   config = {"configurable": {"thread_id": "unique-id"}}
#   result = app.invoke(inputs, config)
#
# Resume after interrupt:
#   result = app.invoke(Command(resume="human's response"), config)
#
# Inspect state:
#   state = app.get_state(config)
#   print(state.values)   # Current state dict
#   print(state.next)     # Next node to run
#
# =============================================================================
