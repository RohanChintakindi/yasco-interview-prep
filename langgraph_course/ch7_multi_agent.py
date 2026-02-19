"""
=====================================================
 CHAPTER 7: MULTI-AGENT WORKFLOWS
=====================================================

WHAT ARE MULTI-AGENT SYSTEMS?
------------------------------
Instead of one LLM doing everything, you have MULTIPLE specialized LLMs
(agents) that collaborate on a task. Each agent has a specific role.

Think of it like a team:
  - RESEARCHER: Finds information
  - WRITER: Drafts content based on research
  - REVIEWER: Critiques the draft and gives feedback

This is powerful because:
  1. Each agent can have a focused system prompt for its role
  2. Different agents can use different models (cheap vs expensive)
  3. The workflow has clear separation of concerns
  4. Agents can iterate (writer -> reviewer -> writer -> reviewer...)


PATTERNS:
---------
1. SEQUENTIAL: Agent A -> Agent B -> Agent C -> Done
   (assembly line)

2. SUPERVISOR: Boss agent routes tasks to worker agents
   (manager pattern)

3. COLLABORATIVE LOOP: Writer -> Reviewer -> Writer -> ... -> Done
   (iterative refinement)

We'll build pattern #3: a Writer-Reviewer loop.


INSTALL:
  pip install langgraph langchain-openai python-dotenv


HOW TO RUN:
  python ch7_multi_agent.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0.3,
)


# =============================================================================
# THE PROJECT: BLOG POST WRITER WITH REVIEW LOOP
# =============================================================================
#
# Workflow:
#   1. RESEARCHER: Generates key points about a topic
#   2. WRITER: Writes a blog post from the research
#   3. REVIEWER: Critiques the post, gives feedback
#   4. If feedback says to revise -> back to WRITER (loop)
#   5. If approved -> Done!
#
#   [START] -> [researcher] -> [writer] -> [reviewer]
#                                 ^            |
#                                 |            v
#                                 +-- revise --+
#                                              |
#                                              +-- approve -> [END]


# =============================================================================
# STATE
# =============================================================================

class BlogState(TypedDict):
    topic: str
    research: str
    draft: str
    feedback: str
    history: Annotated[list[str], operator.add]  # Track what happened
    iteration: int
    status: str  # "writing", "reviewing", "approved"


# =============================================================================
# AGENT NODES
# =============================================================================

def researcher(state: BlogState) -> dict:
    """
    RESEARCHER AGENT
    Role: Generate key points and facts about the topic.
    This gives the writer something concrete to work with.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a research assistant. Generate 4-5 key points about "
         "the given topic that would be useful for writing a blog post. "
         "Be specific and factual. Keep each point to 1 sentence."),
        ("human", "Research topic: {topic}"),
    ])
    chain = prompt | llm | StrOutputParser()
    research = chain.invoke({"topic": state["topic"]})

    print(f"\n  [RESEARCHER] Generated key points")
    return {
        "research": research,
        "history": ["Researcher generated key points"],
    }


def writer(state: BlogState) -> dict:
    """
    WRITER AGENT
    Role: Write or revise a blog post based on research and feedback.
    """
    iteration = state.get("iteration", 0) + 1
    feedback = state.get("feedback", "")

    if feedback and iteration > 1:
        # REVISION: incorporate feedback
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a blog writer. Revise the draft based on the reviewer's "
             "feedback. Keep the post concise (3-4 short paragraphs)."),
            ("human",
             "Topic: {topic}\n\n"
             "Research:\n{research}\n\n"
             "Current draft:\n{draft}\n\n"
             "Reviewer feedback:\n{feedback}\n\n"
             "Write an improved version:"),
        ])
        chain = prompt | llm | StrOutputParser()
        draft = chain.invoke({
            "topic": state["topic"],
            "research": state["research"],
            "draft": state["draft"],
            "feedback": feedback,
        })
        print(f"  [WRITER] Revised draft (v{iteration})")
    else:
        # FIRST DRAFT
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a blog writer. Write a concise blog post (3-4 short "
             "paragraphs) based on the research provided. Make it engaging "
             "and informative."),
            ("human",
             "Topic: {topic}\n\n"
             "Research:\n{research}\n\n"
             "Write the blog post:"),
        ])
        chain = prompt | llm | StrOutputParser()
        draft = chain.invoke({
            "topic": state["topic"],
            "research": state["research"],
        })
        print(f"  [WRITER] Wrote first draft")

    return {
        "draft": draft,
        "iteration": iteration,
        "status": "reviewing",
        "history": [f"Writer produced draft v{iteration}"],
    }


def reviewer(state: BlogState) -> dict:
    """
    REVIEWER AGENT
    Role: Critique the draft. Either approve it or give specific feedback.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an editor reviewing a blog post. "
         "Evaluate clarity, accuracy, engagement, and completeness.\n\n"
         "If the post is GOOD ENOUGH (doesn't need to be perfect), "
         "respond with exactly: APPROVED\n\n"
         "If it needs improvement, give 1-2 specific, actionable suggestions. "
         "Be concise. Don't ask for perfection - approve when it's good enough."),
        ("human",
         "Topic: {topic}\n\n"
         "Draft (v{iteration}):\n{draft}\n\n"
         "Your review:"),
    ])
    chain = prompt | llm | StrOutputParser()
    review = chain.invoke({
        "topic": state["topic"],
        "draft": state["draft"],
        "iteration": state["iteration"],
    })

    is_approved = "APPROVED" in review.upper()

    if is_approved:
        print(f"  [REVIEWER] APPROVED!")
    else:
        print(f"  [REVIEWER] Feedback: {review[:80]}...")

    return {
        "feedback": review,
        "status": "approved" if is_approved else "writing",
        "history": [f"Reviewer: {'APPROVED' if is_approved else 'Requested revision'}"],
    }


# =============================================================================
# ROUTING FUNCTION
# =============================================================================

def review_router(state: BlogState) -> str:
    """After review: approve (END) or revise (loop back to writer)."""
    if state["status"] == "approved":
        return END
    if state["iteration"] >= 3:
        # Safety: max 3 iterations to prevent infinite loops
        return END
    return "writer"  # Loop back!


# =============================================================================
# BUILD THE GRAPH
# =============================================================================

print("=" * 60)
print("MULTI-AGENT BLOG WRITER")
print("=" * 60)

graph = StateGraph(BlogState)

graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.add_node("reviewer", reviewer)

graph.add_edge(START, "researcher")     # Start with research
graph.add_edge("researcher", "writer")  # Research -> Writer
graph.add_edge("writer", "reviewer")    # Writer -> Reviewer
graph.add_conditional_edges("reviewer", review_router)  # Review -> loop or done

app = graph.compile()

# =============================================================================
# RUN IT!
# =============================================================================

result = app.invoke({
    "topic": "Why Python is great for beginners",
    "research": "",
    "draft": "",
    "feedback": "",
    "history": [],
    "iteration": 0,
    "status": "writing",
})

print(f"\n{'=' * 60}")
print(f"FINAL BLOG POST (after {result['iteration']} draft(s)):")
print(f"{'=' * 60}")
print(result["draft"])
print(f"\n{'=' * 60}")
print(f"Workflow history:")
for step in result["history"]:
    print(f"  - {step}")
print()


# =============================================================================
# OTHER MULTI-AGENT PATTERNS
# =============================================================================
#
# PATTERN 1: SUPERVISOR
# ----------------------
# A "boss" agent routes tasks to specialized workers:
#
#   [supervisor] -> "this is a math question" -> [math_agent]
#                -> "this needs research"     -> [research_agent]
#                -> "write some code"         -> [code_agent]
#
# The supervisor is an LLM that classifies the task and picks the worker.
#
#
# PATTERN 2: PARALLEL AGENTS
# ---------------------------
# Multiple agents work simultaneously on different aspects:
#
#   [START] -> [pros_agent] ─┐
#           -> [cons_agent] ─┤─> [synthesizer] -> [END]
#           -> [data_agent] ─┘
#
# Three agents research in parallel, then a fourth combines results.
#
#
# PATTERN 3: DEBATE
# -----------------
# Two agents argue opposing views until they reach consensus:
#
#   [agent_for] -> [agent_against] -> [judge]
#       ^                                |
#       └── no consensus ────────────────┘
#
# Useful for exploring ideas from multiple angles.


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Multi-agent workflow steps:
#   1. Define state (what data agents share)
#   2. Define agent nodes (each with its own system prompt/role)
#   3. Define routing logic (who goes next, when to loop/stop)
#   4. Build graph (nodes + edges)
#   5. Compile and run
#
# Tips:
#   - Give each agent a clear, focused system prompt
#   - Track iterations to prevent infinite loops
#   - Use history/logs to debug agent interactions
#   - Start simple (2 agents) and add complexity gradually
#
# =============================================================================
