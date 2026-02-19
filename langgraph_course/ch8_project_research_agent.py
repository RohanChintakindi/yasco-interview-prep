"""
=====================================================
 CHAPTER 8: FINAL PROJECT - RESEARCH AGENT
=====================================================

THE CAPSTONE PROJECT
--------------------
We're building a RESEARCH AGENT that:
  1. Takes a topic from the user
  2. Searches for information (using tools)
  3. Evaluates if it has enough info
  4. If not, searches again with refined queries (LOOP)
  5. Once satisfied, writes a summary
  6. Presents the summary with sources

This combines EVERYTHING from the course:
  - State management (Ch2)
  - Conditional edges & loops (Ch3)
  - Tool calling (Ch4)
  - Custom agent graph (Ch6)
  - Multi-step workflow (Ch7)


ARCHITECTURE:
  ┌─────────────────────────────────────────────────┐
  │                                                 │
  │  [START]                                        │
  │     |                                           │
  │     v                                           │
  │  [planner]  Decides what to search for          │
  │     |                                           │
  │     v                                           │
  │  [researcher]  Searches for information         │
  │     |                                           │
  │     v                                           │
  │  [evaluator]  Enough info? ──> No ──┐           │
  │     |                               |           │
  │     v (Yes)                         v           │
  │  [writer]                      [planner] LOOP   │
  │     |                                           │
  │     v                                           │
  │  [END]                                          │
  │                                                 │
  └─────────────────────────────────────────────────┘


INSTALL:
  pip install langgraph langchain-openai python-dotenv


HOW TO RUN:
  python ch8_project_research_agent.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0.2,
)


# =============================================================================
# TOOLS
# =============================================================================
# In a real app, these would call actual APIs (Google Search, Wikipedia API,
# news API, etc.). Here we simulate with a knowledge base.

KNOWLEDGE_BASE = {
    "python history": (
        "Python was created by Guido van Rossum and first released in 1991. "
        "It was named after Monty Python's Flying Circus. Python 2.0 was released "
        "in 2000 with list comprehensions and garbage collection. Python 3.0 was "
        "released in 2008 as a backwards-incompatible version."
    ),
    "python features": (
        "Python features dynamic typing, automatic memory management, and supports "
        "multiple programming paradigms including procedural, object-oriented, and "
        "functional programming. It has a comprehensive standard library often called "
        "'batteries included'. Python uses indentation for code blocks."
    ),
    "python popularity": (
        "Python is consistently ranked among the top 3 programming languages worldwide. "
        "It is the most popular language for data science and machine learning. "
        "Major companies using Python include Google, Netflix, Instagram, and Spotify. "
        "The Python Package Index (PyPI) hosts over 500,000 packages."
    ),
    "python ai": (
        "Python dominates the AI/ML ecosystem with libraries like TensorFlow, PyTorch, "
        "scikit-learn, and Hugging Face Transformers. LangChain and LangGraph are Python "
        "frameworks for building LLM applications. Jupyter notebooks, a key data science "
        "tool, run Python natively."
    ),
    "python web": (
        "Python web frameworks include Django (full-featured), Flask (lightweight), "
        "and FastAPI (modern, async). Django powers Instagram and Pinterest. "
        "Flask is popular for microservices and APIs. FastAPI is the fastest-growing "
        "Python web framework, known for automatic API documentation."
    ),
    "langgraph": (
        "LangGraph is a library by LangChain Inc for building stateful, multi-agent "
        "AI applications. It models workflows as graphs with nodes, edges, and state. "
        "Key features include conditional edges, human-in-the-loop, and checkpointing."
    ),
    "artificial intelligence": (
        "Artificial Intelligence is the simulation of human intelligence by machines. "
        "Modern AI is dominated by deep learning and large language models. "
        "Key milestones include DeepBlue (1997), AlphaGo (2016), and ChatGPT (2022). "
        "AI is used in healthcare, autonomous vehicles, finance, and creative arts."
    ),
}


@tool
def search_web(query: str) -> str:
    """Search the web for information about a topic. Returns relevant text."""
    query_lower = query.lower()
    results = []
    for key, value in KNOWLEDGE_BASE.items():
        # Check if any word in the query matches a key
        if any(word in key for word in query_lower.split()):
            results.append(value)

    if results:
        return "\n\n".join(results)
    return f"No results found for: {query}"


# =============================================================================
# STATE
# =============================================================================

class ResearchState(TypedDict):
    topic: str                                          # What to research
    search_queries: Annotated[list[str], operator.add]  # Queries we've made
    findings: Annotated[list[str], operator.add]        # What we've found
    iteration: int                                      # Loop counter
    has_enough_info: bool                               # Evaluator's decision
    summary: str                                        # Final output
    log: Annotated[list[str], operator.add]             # Step-by-step log


# =============================================================================
# NODES
# =============================================================================

def planner(state: ResearchState) -> dict:
    """
    PLANNER: Decides what search queries to make.
    On first run: generates initial queries.
    On subsequent runs: generates follow-up queries based on gaps.
    """
    iteration = state.get("iteration", 0) + 1
    existing_findings = "\n".join(state.get("findings", []))

    if iteration == 1:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a research planner. Given a topic, generate 2-3 specific "
             "search queries to gather comprehensive information. "
             "Return ONLY the queries, one per line. No numbering or bullets."),
            ("human", "Topic: {topic}"),
        ])
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"topic": state["topic"]})
    else:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a research planner. We already have some findings but need more. "
             "Generate 1-2 NEW search queries to fill gaps. "
             "Return ONLY the queries, one per line."),
            ("human",
             "Topic: {topic}\n\n"
             "Existing findings:\n{findings}\n\n"
             "Previous queries: {queries}\n\n"
             "What else should we search for?"),
        ])
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({
            "topic": state["topic"],
            "findings": existing_findings,
            "queries": ", ".join(state.get("search_queries", [])),
        })

    queries = [q.strip() for q in result.strip().split("\n") if q.strip()]
    print(f"  [PLANNER] Iteration {iteration}, queries: {queries}")

    return {
        "search_queries": queries,
        "iteration": iteration,
        "log": [f"Planner (iter {iteration}): generated queries: {queries}"],
    }


def researcher(state: ResearchState) -> dict:
    """
    RESEARCHER: Executes search queries and collects findings.
    """
    new_queries = state["search_queries"][-3:]  # Use the latest queries
    new_findings = []

    for query in new_queries:
        result = search_web.invoke(query)
        if "No results found" not in result:
            new_findings.append(f"[Query: {query}]\n{result}")

    found_count = len(new_findings)
    print(f"  [RESEARCHER] Found {found_count} results")

    return {
        "findings": new_findings,
        "log": [f"Researcher: searched {len(new_queries)} queries, got {found_count} results"],
    }


def evaluator(state: ResearchState) -> dict:
    """
    EVALUATOR: Decides if we have enough information to write a summary.
    """
    all_findings = "\n\n".join(state.get("findings", []))

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are evaluating whether we have enough research to write a comprehensive "
         "summary about a topic. Consider: Do we have enough breadth and depth?\n\n"
         "Respond with ONLY 'SUFFICIENT' or 'INSUFFICIENT' followed by a brief reason."),
        ("human",
         "Topic: {topic}\n\n"
         "Research gathered so far:\n{findings}\n\n"
         "Is this sufficient?"),
    ])
    chain = prompt | llm | StrOutputParser()
    evaluation = chain.invoke({
        "topic": state["topic"],
        "findings": all_findings,
    })

    has_enough = "SUFFICIENT" in evaluation.upper()
    print(f"  [EVALUATOR] {'SUFFICIENT' if has_enough else 'INSUFFICIENT'}")

    return {
        "has_enough_info": has_enough,
        "log": [f"Evaluator: {'SUFFICIENT' if has_enough else 'INSUFFICIENT'} - {evaluation[:60]}"],
    }


def writer(state: ResearchState) -> dict:
    """
    WRITER: Synthesizes all findings into a final summary.
    """
    all_findings = "\n\n".join(state.get("findings", []))

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a writer. Synthesize the research findings into a clear, "
         "well-organized summary. Use paragraphs with clear topics. "
         "Be informative and concise. 3-5 paragraphs."),
        ("human",
         "Topic: {topic}\n\n"
         "Research findings:\n{findings}\n\n"
         "Write the summary:"),
    ])
    chain = prompt | llm | StrOutputParser()
    summary = chain.invoke({
        "topic": state["topic"],
        "findings": all_findings,
    })

    print(f"  [WRITER] Wrote summary ({len(summary)} chars)")

    return {
        "summary": summary,
        "log": [f"Writer: produced final summary ({len(summary)} chars)"],
    }


# =============================================================================
# ROUTING
# =============================================================================

def should_continue_research(state: ResearchState) -> str:
    """After evaluation: write summary or research more."""
    if state["has_enough_info"]:
        return "writer"
    if state["iteration"] >= 3:
        # Safety limit
        print("  [ROUTER] Max iterations reached, moving to writer")
        return "writer"
    return "planner"  # LOOP: plan more queries


# =============================================================================
# BUILD THE GRAPH
# =============================================================================

graph = StateGraph(ResearchState)

graph.add_node("planner", planner)
graph.add_node("researcher", researcher)
graph.add_node("evaluator", evaluator)
graph.add_node("writer", writer)

graph.add_edge(START, "planner")
graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "evaluator")
graph.add_conditional_edges("evaluator", should_continue_research)
graph.add_edge("writer", END)

app = graph.compile()


# =============================================================================
# RUN THE RESEARCH AGENT
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  RESEARCH AGENT")
    print("=" * 60)

    topic = "Python programming language"

    print(f"\n  Researching: '{topic}'")
    print(f"  {'─' * 50}\n")

    result = app.invoke({
        "topic": topic,
        "search_queries": [],
        "findings": [],
        "iteration": 0,
        "has_enough_info": False,
        "summary": "",
        "log": [],
    })

    print(f"\n{'=' * 60}")
    print("RESEARCH SUMMARY")
    print(f"{'=' * 60}")
    print(result["summary"])

    print(f"\n{'=' * 60}")
    print("EXECUTION LOG")
    print(f"{'=' * 60}")
    for entry in result["log"]:
        print(f"  - {entry}")

    print(f"\nTotal iterations: {result['iteration']}")
    print(f"Total findings: {len(result['findings'])}")
    print(f"Total queries: {len(result['search_queries'])}")


# =============================================================================
# WHAT YOU'VE LEARNED - THE COMPLETE LANGGRAPH JOURNEY
# =============================================================================
#
# Ch1:  What is LangGraph
#       Graphs vs chains, nodes + edges + state, your first graph
#
# Ch2:  State Deep Dive
#       TypedDict, reducers, append vs replace, MessagesState
#
# Ch3:  Conditional Edges
#       Branching, looping, routing functions, self-correcting LLM
#
# Ch4:  Tool-Calling Agents
#       @tool, create_react_agent, the ReAct loop
#
# Ch5:  Human-in-the-Loop
#       interrupt(), checkpoints, threads, MemorySaver
#
# Ch6:  Custom Agent from Scratch
#       bind_tools, ToolNode, manual agent loop
#
# Ch7:  Multi-Agent Workflows
#       Specialized agents, writer-reviewer loop, patterns
#
# Ch8:  Final Project
#       Research agent: planner -> researcher -> evaluator -> writer
#       With loops, tool use, and multi-step reasoning
#
#
# WHERE TO GO NEXT:
# -----------------
# 1. Add REAL tools (web search API, Wikipedia API, database queries)
# 2. Add human-in-the-loop (pause for approval before writing)
# 3. Add persistence (SqliteSaver to save state across restarts)
# 4. Build a web UI with Streamlit/Gradio
# 5. Explore LangGraph Cloud for deployment
# 6. Combine with RAG (langchain_course) for document-grounded agents
#
# =============================================================================
