"""
=====================================================
 CHAPTER 3: CONDITIONAL EDGES - BRANCHING & LOOPING
=====================================================

THIS IS WHERE LANGGRAPH SHINES.
This is what you CAN'T do with LangChain chains.

In Chapters 1-2, every edge was a straight line: A -> B -> C.
But real workflows need DECISIONS:

  "If the answer is good enough, stop. Otherwise, try again."
  "If the user wants a summary, go to summarizer. If they want code, go to coder."

Conditional edges are functions that LOOK AT THE STATE and decide
which node to go to next. This enables:

  LOOPS:      Try -> Check -> Not good? -> Try again -> Check -> Good! -> Done
  BRANCHING:  Classify -> Is it spam? -> Yes: delete. No: deliver.
  ROUTING:    Parse intent -> "search" -> search_node
                           -> "calculate" -> calc_node
                           -> "chat" -> chat_node


INSTALL:
  pip install langgraph langchain-openai python-dotenv


HOW TO RUN:
  python ch3_conditional_edges.py
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator
import random


# =============================================================================
# PART 1: CONDITIONAL EDGES - THE BASICS
# =============================================================================
#
# add_conditional_edges(source_node, routing_function)
#
# The routing function:
#   - Receives the current state
#   - Returns the NAME of the next node (a string)
#   - Or returns END to stop the graph
#
# Think of it like a railroad switch: the train reaches a junction,
# and the routing function decides which track to take.

print("=" * 60)
print("PART 1: Basic conditional edge")
print("=" * 60)


class GradeState(TypedDict):
    score: int
    result: str


def check_score(state: GradeState) -> dict:
    """Just passes the score through (it's already in state)."""
    return {}


def pass_student(state: GradeState) -> dict:
    return {"result": f"PASSED with score {state['score']}!"}


def fail_student(state: GradeState) -> dict:
    return {"result": f"FAILED with score {state['score']}. Study harder!"}


# The ROUTING FUNCTION: decides which node comes next
def grade_router(state: GradeState) -> str:
    """
    This function looks at the state and returns the NAME
    of the next node to run.
    """
    if state["score"] >= 60:
        return "pass"   # Go to pass_student node
    else:
        return "fail"   # Go to fail_student node


# Build the graph
graph = StateGraph(GradeState)
graph.add_node("check", check_score)
graph.add_node("pass", pass_student)
graph.add_node("fail", fail_student)

graph.add_edge(START, "check")

# CONDITIONAL EDGE: after "check", call grade_router to decide next step
graph.add_conditional_edges("check", grade_router)

graph.add_edge("pass", END)
graph.add_edge("fail", END)

app = graph.compile()

# Test with different scores:
for score in [85, 42, 60, 15]:
    result = app.invoke({"score": score, "result": ""})
    print(f"  Score {score}: {result['result']}")

print()

# The graph:
#              ┌──> [pass] ──> END
#   START ──> [check]
#              └──> [fail] ──> END
#
# The routing function decides which branch to take!


# =============================================================================
# PART 2: LOOPS - THE KILLER FEATURE
# =============================================================================
#
# A loop happens when a conditional edge points BACK to an earlier node.
# This is something chains literally cannot do.
#
# Pattern:
#   do_work -> check_quality -> good? -> END
#                             -> bad?  -> do_work (LOOP BACK)

print("=" * 60)
print("PART 2: Loops - retrying until success")
print("=" * 60)


class RetryState(TypedDict):
    target: int                              # Number we're trying to guess
    attempts: Annotated[list[int], operator.add]  # History of guesses
    iteration: int                           # How many tries
    success: bool


def guess(state: RetryState) -> dict:
    """Make a random guess between 1 and 10."""
    g = random.randint(1, 10)
    iteration = state.get("iteration", 0) + 1
    print(f"    Attempt {iteration}: guessed {g} (target: {state['target']})")
    return {
        "attempts": [g],
        "iteration": iteration,
    }


def check(state: RetryState) -> dict:
    """Check if the latest guess was correct."""
    latest_guess = state["attempts"][-1]
    success = latest_guess == state["target"]
    return {"success": success}


def should_continue(state: RetryState) -> str:
    """Routing function: keep guessing or stop?"""
    if state["success"]:
        return END          # Correct! Stop.
    if state["iteration"] >= 10:
        return END          # Too many tries. Give up.
    return "guess"          # Wrong. Try again! (LOOP)


graph = StateGraph(RetryState)
graph.add_node("guess", guess)
graph.add_node("check", check)

graph.add_edge(START, "guess")
graph.add_edge("guess", "check")
graph.add_conditional_edges("check", should_continue)  # Loop or END

app = graph.compile()

random.seed(42)  # For reproducible results
result = app.invoke({
    "target": 7,
    "attempts": [],
    "iteration": 0,
    "success": False,
})

print(f"  All attempts: {result['attempts']}")
print(f"  Success: {result['success']}")
print(f"  Took {result['iteration']} tries")
print()

# The graph:
#   START -> [guess] -> [check] -> success? -> END
#                         |
#                         └── not yet ──> [guess]  (LOOP!)
#
# This loop continues until we guess right or hit 10 attempts.
# THIS is what makes LangGraph special.


# =============================================================================
# PART 3: MULTI-WAY ROUTING
# =============================================================================
#
# Conditional edges aren't limited to two options.
# The routing function can return any node name.

print("=" * 60)
print("PART 3: Multi-way routing (3+ branches)")
print("=" * 60)


class TaskState(TypedDict):
    task_type: str
    result: str


def classify(state: TaskState) -> dict:
    return {}  # task_type is already in state


def handle_math(state: TaskState) -> dict:
    return {"result": "Solved: 2 + 2 = 4"}


def handle_text(state: TaskState) -> dict:
    return {"result": "Here's your text summary."}


def handle_code(state: TaskState) -> dict:
    return {"result": "def hello(): print('Hello!')"}


def handle_unknown(state: TaskState) -> dict:
    return {"result": "I don't know how to handle that."}


def route_task(state: TaskState) -> str:
    """Route to the appropriate handler based on task type."""
    task = state["task_type"]
    if task == "math":
        return "math"
    elif task == "text":
        return "text"
    elif task == "code":
        return "code"
    else:
        return "unknown"


graph = StateGraph(TaskState)
graph.add_node("classify", classify)
graph.add_node("math", handle_math)
graph.add_node("text", handle_text)
graph.add_node("code", handle_code)
graph.add_node("unknown", handle_unknown)

graph.add_edge(START, "classify")
graph.add_conditional_edges("classify", route_task)
graph.add_edge("math", END)
graph.add_edge("text", END)
graph.add_edge("code", END)
graph.add_edge("unknown", END)

app = graph.compile()

for task in ["math", "code", "text", "other"]:
    result = app.invoke({"task_type": task, "result": ""})
    print(f"  Task '{task}': {result['result']}")

print()

# The graph:
#                ┌──> [math]    ──> END
#                ├──> [text]    ──> END
#   START ──> [classify]
#                ├──> [code]    ──> END
#                └──> [unknown] ──> END


# =============================================================================
# PART 4: LOOPS WITH LLMs - SELF-CORRECTING AGENT
# =============================================================================
#
# Now let's combine loops with actual LLM calls.
# This is a pattern you'll use ALL the time:
#   Generate -> Evaluate -> Good? Done. Bad? Regenerate.

print("=" * 60)
print("PART 4: Self-correcting LLM (loop with LLM)")
print("=" * 60)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0.7,
)


class WriterState(TypedDict):
    topic: str
    draft: str
    feedback: str
    iteration: int
    is_good: bool


def write_draft(state: WriterState) -> dict:
    """LLM writes or revises a draft."""
    iteration = state.get("iteration", 0) + 1
    feedback = state.get("feedback", "")

    if feedback:
        prompt = ChatPromptTemplate.from_template(
            "You wrote this draft about {topic}:\n\n{draft}\n\n"
            "The reviewer said: {feedback}\n\n"
            "Write an improved version. Keep it to 2-3 sentences."
        )
        chain = prompt | llm | StrOutputParser()
        draft = chain.invoke({
            "topic": state["topic"],
            "draft": state["draft"],
            "feedback": feedback,
        })
    else:
        prompt = ChatPromptTemplate.from_template(
            "Write a 2-3 sentence paragraph about {topic}."
        )
        chain = prompt | llm | StrOutputParser()
        draft = chain.invoke({"topic": state["topic"]})

    print(f"  [Draft v{iteration}]: {draft[:80]}...")
    return {"draft": draft, "iteration": iteration}


def review_draft(state: WriterState) -> dict:
    """LLM reviews the draft and gives feedback."""
    prompt = ChatPromptTemplate.from_template(
        "Review this short paragraph about {topic}. "
        "Is it clear and informative?\n\n"
        "Paragraph: {draft}\n\n"
        "Reply with ONLY 'APPROVED' if it's good, or give brief feedback to improve it."
    )
    chain = prompt | llm | StrOutputParser()
    review = chain.invoke({"topic": state["topic"], "draft": state["draft"]})
    is_good = "APPROVED" in review.upper()
    print(f"  [Review]: {'APPROVED' if is_good else review[:60]}...")
    return {"feedback": review, "is_good": is_good}


def should_revise(state: WriterState) -> str:
    if state["is_good"]:
        return END
    if state["iteration"] >= 3:  # Max 3 revisions
        return END
    return "write"  # LOOP back to write!


graph = StateGraph(WriterState)
graph.add_node("write", write_draft)
graph.add_node("review", review_draft)

graph.add_edge(START, "write")
graph.add_edge("write", "review")
graph.add_conditional_edges("review", should_revise)

app = graph.compile()

result = app.invoke({
    "topic": "why Python is popular",
    "draft": "",
    "feedback": "",
    "iteration": 0,
    "is_good": False,
})

print(f"\n  Final draft (v{result['iteration']}): {result['draft']}")
print(f"  Approved: {result['is_good']}")
print()


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
#
# 1. add_conditional_edges(node, router_fn) adds decision points
# 2. Router function: reads state, returns next node name (or END)
# 3. LOOPS: router points back to an earlier node
# 4. BRANCHING: router picks one of multiple forward paths
# 5. Always add a max iteration check to prevent infinite loops!
# 6. Pattern: Generate -> Evaluate -> Loop or Done
#    This is THE core pattern for self-correcting AI agents
#
# =============================================================================
