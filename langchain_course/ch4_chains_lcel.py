"""
=====================================================
 CHAPTER 4: CHAINS & LCEL (LangChain Expression Language)
=====================================================

WHAT WE KNOW SO FAR
--------------------
We've been using the | pipe operator:
  prompt | llm | parser

This is LCEL - LangChain Expression Language. It's not just a cute syntax.
It's the core abstraction of LangChain. Understanding LCEL deeply is what
separates someone who "uses" LangChain from someone who BUILDS with it.


WHAT IS A CHAIN?
----------------
A chain is just a sequence of Runnables connected with |.
When you call .invoke() on a chain, data flows through each step:

  {"topic": "AI"} -> [Prompt] -> [LLM] -> [Parser] -> "AI is..."

Each step:
  1. Receives the output of the previous step
  2. Does its thing
  3. Passes its output to the next step

That's it. But the power comes from the building blocks you can use
BETWEEN the steps: custom functions, parallel execution, routing, etc.


HOW TO RUN THIS FILE:
  python ch4_chains_lcel.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0.2,
)


# =============================================================================
# PART 1: BASIC CHAIN (RECAP)
# =============================================================================

print("=" * 60)
print("PART 1: Basic Chain")
print("=" * 60)

chain = (
    ChatPromptTemplate.from_template("Explain {topic} in one sentence.")
    | llm
    | StrOutputParser()
)

# What happens when we call .invoke():
#   Step 1: Prompt receives {"topic": "recursion"}
#           -> outputs [HumanMessage("Explain recursion in one sentence.")]
#   Step 2: LLM receives those messages
#           -> outputs AIMessage("Recursion is when a function calls itself...")
#   Step 3: StrOutputParser receives the AIMessage
#           -> outputs "Recursion is when a function calls itself..."

print(chain.invoke({"topic": "recursion"}))
print()

# The chain itself is a Runnable, so it has .invoke(), .stream(), .batch() too!
# This means chains can be NESTED inside other chains. Runnables all the way down.


# =============================================================================
# PART 2: RunnableLambda - CUSTOM FUNCTIONS IN CHAINS
# =============================================================================
#
# What if you need to do something custom between steps?
# Like transform data, log something, clean text, or call an API?
#
# You can't just stick a regular Python function in a chain:
#   prompt | llm | my_function | parser    # ERROR! my_function isn't a Runnable
#
# RunnableLambda WRAPS a function to make it a Runnable:
#   prompt | llm | RunnableLambda(my_function) | parser   # Works!
#
# Your function takes one argument (the input from the previous step)
# and returns one value (the output to the next step).

print("=" * 60)
print("PART 2: RunnableLambda - Custom functions in chains")
print("=" * 60)


def shout(text: str) -> str:
    """Convert text to uppercase with exclamation marks."""
    return text.upper() + "!!!"


def word_count(text: str) -> str:
    """Add a word count to the text."""
    count = len(text.split())
    return f"{text}\n\n[Word count: {count}]"


# Chain: get response -> uppercase it -> add word count
chain = (
    ChatPromptTemplate.from_template("Give a 1-sentence motivational quote about {topic}")
    | llm
    | StrOutputParser()
    | RunnableLambda(shout)
    | RunnableLambda(word_count)
)

print(chain.invoke({"topic": "perseverance"}))
print()

# SHORTHAND: You can also use a decorator or inline lambda:
chain = (
    ChatPromptTemplate.from_template("What is {topic}?")
    | llm
    | StrOutputParser()
    | RunnableLambda(lambda text: text[:50] + "...")  # Truncate to 50 chars
)

print(chain.invoke({"topic": "the universe"}))
print()


# =============================================================================
# PART 3: RunnablePassthrough - "JUST PASS IT THROUGH"
# =============================================================================
#
# Sometimes you need the original input to SKIP past some steps and
# arrive later in the chain unchanged.
#
# RunnablePassthrough() is a Runnable that does nothing: it receives
# input and outputs the EXACT same thing.
#
# "Why would I want a component that does nothing?"
#
# Because of how it combines with dicts (Part 4). Hang tight.

print("=" * 60)
print("PART 3: RunnablePassthrough")
print("=" * 60)

# Simple use: pass a string directly instead of wrapping it in a dict
chain = (
    {"topic": RunnablePassthrough()}
    | ChatPromptTemplate.from_template("Define {topic} in one sentence.")
    | llm
    | StrOutputParser()
)

# Normally you'd call chain.invoke({"topic": "entropy"})
# But with RunnablePassthrough, the input STRING becomes the "topic" value:
print(chain.invoke("entropy"))
print()

# What happened:
#   "entropy" -> {"topic": RunnablePassthrough()} -> {"topic": "entropy"}
#   The passthrough took "entropy" and placed it as the "topic" value.


# =============================================================================
# PART 4: RunnableParallel / DICTS - RUNNING STEPS SIDE BY SIDE
# =============================================================================
#
# This is WHERE LCEL GETS REALLY POWERFUL.
#
# A dict in LCEL is secretly a RunnableParallel. It runs multiple
# Runnables AT THE SAME TIME and collects results into a dict.
#
# {
#     "key_a": runnable_1,   <- runs in parallel
#     "key_b": runnable_2,   <- runs in parallel
# }
#
# Input goes to BOTH runnables. Each produces a value. You get:
# {"key_a": result_1, "key_b": result_2}
#
# This is CRITICAL for RAG (you'll see in Chapter 9):
# you need to run retrieval AND pass the question at the same time.

print("=" * 60)
print("PART 4: RunnableParallel - Multiple steps at once")
print("=" * 60)

# Two separate chains that do different things:
joke_chain = (
    ChatPromptTemplate.from_template("Tell a very short joke about {topic}")
    | llm
    | StrOutputParser()
)

fact_chain = (
    ChatPromptTemplate.from_template("Tell me one fun fact about {topic}")
    | llm
    | StrOutputParser()
)

# RunnableParallel runs them simultaneously:
parallel = RunnableParallel(
    joke=joke_chain,
    fact=fact_chain,
)

result = parallel.invoke({"topic": "dogs"})

# result is a dict with both results:
print(f"Joke: {result['joke']}")
print()
print(f"Fact: {result['fact']}")
print()

# This is faster than running them one after another, because both
# API calls happen at the same time.

# DICT SHORTHAND - This does the same thing:
parallel = {
    "joke": joke_chain,
    "fact": fact_chain,
}
# When LangChain sees a dict in a chain, it automatically treats it
# as a RunnableParallel.


# =============================================================================
# PART 5: CHAIN OF CHAINS (COMPOSITION)
# =============================================================================
#
# Since a chain IS a Runnable, you can use it inside another chain.
# This lets you build complex pipelines from simple pieces.
#
# Think of it like functions calling functions:
#   def step1(): ...
#   def step2(): ...
#   def pipeline(): return step2(step1())
#
# But with Runnables:
#   chain = step1_chain | adapter | step2_chain

print("=" * 60)
print("PART 5: Chain of chains")
print("=" * 60)

# Chain 1: Generate a random topic
topic_chain = (
    ChatPromptTemplate.from_template(
        "Give me one interesting science topic in 2-3 words. "
        "Reply with ONLY the topic, nothing else."
    )
    | llm
    | StrOutputParser()
)

# Chain 2: Explain a given topic
explain_chain = (
    ChatPromptTemplate.from_template(
        "Explain {topic} to a 5-year-old in 2 sentences."
    )
    | llm
    | StrOutputParser()
)

# Problem: topic_chain outputs a STRING ("black holes")
# But explain_chain expects a DICT ({"topic": "black holes"})
# We need an adapter: convert string -> dict

full_chain = (
    topic_chain
    | RunnableLambda(lambda topic: {"topic": topic})  # string -> dict adapter
    | explain_chain
)

result = full_chain.invoke({})
print(f"Result: {result}")
print()

# What happened:
#   {} -> topic_chain -> "quantum entanglement"
#   "quantum entanglement" -> lambda -> {"topic": "quantum entanglement"}
#   {"topic": "quantum entanglement"} -> explain_chain -> "Imagine you have..."


# =============================================================================
# PART 6: THE RAG PATTERN (PREVIEW)
# =============================================================================
#
# This is the MOST IMPORTANT pattern in LangChain. It's how RAG works.
# Let's preview it now so you recognize it when we build real RAG in Ch9.
#
# The pattern: use a DICT to run retrieval and passthrough in parallel,
# then feed both into a prompt.

print("=" * 60)
print("PART 6: The RAG Pattern (preview)")
print("=" * 60)

# Fake "retriever" - in reality this would search a vector database
def fake_retrieve(question: str) -> str:
    """Pretend we searched a database and found this context."""
    knowledge = {
        "python": "Python was created by Guido van Rossum in 1991.",
        "javascript": "JavaScript was created by Brendan Eich in 1995.",
    }
    # Return first matching knowledge, or a default
    for key, value in knowledge.items():
        if key in question.lower():
            return value
    return "No relevant information found."


# The RAG chain:
rag_chain = (
    {
        # These run IN PARALLEL:
        "context": RunnableLambda(lambda x: fake_retrieve(x["question"])),
        "question": RunnableLambda(lambda x: x["question"]),
    }
    | ChatPromptTemplate.from_template(
        "Answer the question based ONLY on this context:\n"
        "Context: {context}\n\n"
        "Question: {question}"
    )
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke({"question": "Who created Python?"}))
print()
print(rag_chain.invoke({"question": "When was JavaScript made?"}))
print()

# In Chapters 5-9, we'll replace fake_retrieve with a REAL retriever
# that searches actual documents using embeddings. But the chain
# structure will look almost identical to this.


# =============================================================================
# PART 7: .bind() - ATTACHING CONFIG TO A RUNNABLE
# =============================================================================
#
# Sometimes you want to modify a Runnable's behavior without changing
# the chain structure. .bind() lets you "attach" extra parameters.
#
# Think of it like setting default arguments on a function.

print("=" * 60)
print("PART 7: .bind() - Attaching config")
print("=" * 60)

# Example: make the LLM stop generating after a period
chain = (
    ChatPromptTemplate.from_template("What is {topic}?")
    | llm.bind(stop=["\n"])  # Stop at the first newline
    | StrOutputParser()
)

result = chain.invoke({"topic": "the moon"})
print(f"Stopped at newline: {result}")
print()

# .bind() is useful for:
#   - Setting stop sequences
#   - Changing max_tokens for specific calls
#   - Any parameter the LLM accepts


# =============================================================================
# CHEAT SHEET: LCEL BUILDING BLOCKS
# =============================================================================
#
# COMPONENT              | INPUT        | OUTPUT       | WHAT IT DOES
# -----------------------+--------------+--------------+---------------------------
# ChatPromptTemplate     | dict         | messages     | Fills in template variables
# ChatOpenAI (LLM)       | messages/str | AIMessage    | Calls the AI model
# StrOutputParser        | AIMessage    | str          | Extracts .content as string
# RunnableLambda(fn)     | anything     | anything     | Runs your custom function
# RunnablePassthrough()  | anything     | same thing   | Passes input through unchanged
# RunnableParallel / {}  | anything     | dict         | Runs multiple steps in parallel
# chain_a | chain_b      | varies       | varies       | Connects two Runnables
# llm.bind(key=val)      | (same)       | (same)       | Attaches default params
#
# =============================================================================
