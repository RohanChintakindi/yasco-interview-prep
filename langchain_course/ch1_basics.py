"""
===========================================
 CHAPTER 1: THE BASICS - YOUR FIRST LLM CALL
===========================================

WHAT IS LANGCHAIN?
------------------
Imagine you want to build an app that uses AI (like a chatbot, a document
Q&A system, or an AI assistant). You COULD write raw HTTP requests to
OpenAI's API, parse JSON responses, handle errors, manage conversation
history, deal with token limits... all by hand.

Or you could use LangChain.

LangChain is a framework that gives you pre-built building blocks:
  - Need to talk to an LLM? There's a block for that.
  - Need to format a prompt? There's a block for that.
  - Need to load a PDF? There's a block for that.
  - Need to search a database? There's a block for that.

And the magic: all these blocks SNAP TOGETHER like Lego pieces.


THE SINGLE MOST IMPORTANT CONCEPT: RUNNABLES
---------------------------------------------
Before we write any code, you need to understand this one idea because
it's the foundation of EVERYTHING in LangChain:

  ** Every component in LangChain is a "Runnable" **

What does that mean? A Runnable is any object that:
  1. Takes some INPUT
  2. Does something with it
  3. Produces some OUTPUT

And every Runnable has the same methods:
  .invoke(input)   -> Run once, get full result
  .stream(input)   -> Run and get result piece by piece
  .batch([inputs]) -> Run multiple inputs at once
  .ainvoke(input)  -> Async version of invoke

Why does this matter? Because when EVERYTHING has the same interface,
you can chain them together:

  block_a | block_b | block_c

Data flows left to right. Output of block_a becomes input of block_b,
output of block_b becomes input of block_c. That's it. That's LangChain.

Let's see this in practice.


HOW TO RUN THIS FILE:
  python ch1_basics.py
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================
# load_dotenv() reads your .env file and makes those values available
# as environment variables. Your .env file should have:
#
#   OPENAI_API_KEY=your-api-key-here
#
# LangChain's ChatOpenAI automatically looks for OPENAI_API_KEY in
# the environment. You don't need to pass it explicitly.
#
# Why use .env instead of hardcoding? Because:
#   1. You won't accidentally commit your key to Git
#   2. Different environments (dev/prod) can have different keys
#   3. It's the industry standard

load_dotenv()


# =============================================================================
# CREATING THE LLM OBJECT
# =============================================================================
# ChatOpenAI is LangChain's wrapper around any OpenAI-compatible API.
#
# "OpenAI-compatible" means the API uses the same format as OpenAI's API.
# Many providers do this: OpenAI, x.ai (Grok), Groq, Together AI, etc.
# So ChatOpenAI isn't just for OpenAI - it works with any of these.
#
# IMPORTANT: Creating this object does NOT call the API.
# It's like saving a phone number in your contacts - you haven't called yet.
# You're just configuring WHO to call and HOW to call them.

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0.2,
)

# Let's break down each parameter:
#
# model="grok-4-1-fast-non-reasoning"
#   Which AI model to use. Each provider has different models.
#   OpenAI has: gpt-4o, gpt-4o-mini, etc.
#   x.ai has: grok-4-1-fast-non-reasoning, grok-3, etc.
#   Think of it like choosing which brain to use.
#
# base_url="https://api.x.ai/v1"
#   WHERE to send requests. By default, ChatOpenAI sends to OpenAI's servers.
#   By changing this, we redirect to x.ai's servers instead.
#   If you were using actual OpenAI, you'd just leave this out entirely.
#
# temperature=0.2
#   Controls randomness in the output.
#   0.0 = Always gives the most likely response (deterministic, focused)
#   0.5 = Moderate creativity
#   1.0 = Very creative, might say unexpected things
#   For factual tasks: use 0.0-0.3
#   For creative writing: use 0.7-1.0
#   0.2 is a good default for most tasks.


# =============================================================================
# YOUR FIRST LLM CALL: .invoke()
# =============================================================================
# .invoke() is the most basic way to use a Runnable.
# It sends your input, WAITS for the complete response, and returns it.
#
# Think of it like sending a text message and waiting for the full reply.

print("=" * 60)
print("PART 1: .invoke() - Your first LLM call")
print("=" * 60)

response = llm.invoke("What is Python in one sentence?")

# Now here's something CRUCIAL that trips up beginners:
# The response is NOT a string. It's an AIMessage OBJECT.
#
# Why? Because LangChain needs to carry more than just text around.
# An AIMessage contains:
#   - .content       = the actual text response (what you usually want)
#   - .response_metadata = info like token usage, model name, finish reason
#   - .id            = unique identifier for this response
#
# This is a design pattern: rich objects carry more info than plain strings.

print(f"Type of response: {type(response)}")
print(f"  (it's an AIMessage, NOT a string!)")
print()
print(f"The full object: {response}")
print()
print(f"Just the text (.content): {response.content}")
print()

# If you try to do string operations on the response directly, it won't work:
#   response.upper()  # ERROR! AIMessage doesn't have .upper()
#   response.content.upper()  # This works! .content IS a string


# =============================================================================
# EXAMINING THE RESPONSE METADATA
# =============================================================================
# The metadata tells you useful things about the API call.

print("=" * 60)
print("PART 2: Response metadata - What else is in there?")
print("=" * 60)

print(f"Text content: {response.content}")
print(f"Metadata: {response.response_metadata}")
print()

# Inside response_metadata you'll typically find:
#   - token_usage: how many tokens the prompt and response used
#     (tokens ~ words, roughly 1 token = 0.75 words)
#     This is how you track API costs.
#   - model_name: which model actually responded
#   - finish_reason: why the model stopped generating
#     "stop" = it finished naturally
#     "length" = it hit the max token limit (response was cut off)


# =============================================================================
# STREAMING: .stream()
# =============================================================================
# .invoke() waits for the ENTIRE response before returning anything.
# For short responses that's fine, but for long ones it feels slow.
#
# .stream() returns chunks AS THEY'RE GENERATED by the model.
# This is how ChatGPT shows text appearing word by word.
#
# IMPORTANT: .stream() doesn't return AIMessage objects.
# It yields AIMessageChunk objects - small pieces of the response.
# Each chunk has a .content with just a few characters/words.
#
#   .invoke()  -> returns ONE AIMessage (complete response)
#   .stream()  -> yields MANY AIMessageChunks (piece by piece)

print("=" * 60)
print("PART 3: .stream() - Watch the response arrive in real time")
print("=" * 60)

print("Response: ", end="")
for chunk in llm.stream("Count from 1 to 10, separated by commas."):
    # chunk is an AIMessageChunk - a small piece of the response
    # chunk.content might be just "1", or ", ", or "2" etc.
    print(chunk.content, end="", flush=True)

    # end="" means don't add a newline after each chunk
    # flush=True means print immediately (don't wait for a buffer to fill)
    # Together, they make the output appear smoothly, character by character.

print()  # Add a newline at the very end
print()

# TRY THIS: Comment out flush=True and see what happens.
# The output will appear in bursts instead of smoothly.

# You can also COMBINE chunks to rebuild the full response:
#
#   full_text = ""
#   for chunk in llm.stream("Hello"):
#       full_text += chunk.content
#   print(full_text)  # Complete response as a string


# =============================================================================
# BATCH: .batch()
# =============================================================================
# What if you have multiple questions and want to ask them all at once?
# You COULD call .invoke() three times in a loop, but that's sequential:
#   Question 1 -> wait -> Question 2 -> wait -> Question 3 -> wait
#
# .batch() sends them all at once and waits for all responses:
#   Question 1 ─┐
#   Question 2 ─┼─> wait -> All responses at once
#   Question 3 ─┘
#
# Much faster when you have multiple independent questions.

print("=" * 60)
print("PART 4: .batch() - Multiple questions at once")
print("=" * 60)

questions = [
    "What color is the sky? (reply in one word)",
    "What color is grass? (reply in one word)",
    "What color is the sun? (reply in one word)",
]

responses = llm.batch(questions)

# responses is a LIST of AIMessage objects (one per question)
for question, response in zip(questions, responses):
    print(f"Q: {question}")
    print(f"A: {response.content}")
    print()


# =============================================================================
# THE RUNNABLE INTERFACE - WHY THIS MATTERS
# =============================================================================
# You might think: "Okay, invoke/stream/batch. Why is this such a big deal?"
#
# Because EVERY component in LangChain has these same methods:
#
#   llm.invoke("hello")          <- works
#   prompt.invoke({"topic": x})  <- works (Ch2)
#   parser.invoke(ai_message)    <- works (Ch3)
#   chain.invoke({"topic": x})   <- works (Ch4)
#   retriever.invoke("query")    <- works (Ch8)
#
# This means:
#   1. Once you learn .invoke(), you can use ANY component
#   2. Any Runnable can be swapped for another Runnable
#   3. Runnables can be chained: runnable_a | runnable_b | runnable_c
#
# This uniformity is what makes LangChain powerful. It's not about any
# single component - it's about how they all fit together.
#
# In the next chapter, we'll see our second Runnable: PromptTemplates.


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
#   from langchain_openai import ChatOpenAI
#
#   llm = ChatOpenAI(model="...", base_url="...", temperature=0.2)
#
#   # One call, full response:
#   response = llm.invoke("question")
#   text = response.content
#
#   # Streaming:
#   for chunk in llm.stream("question"):
#       print(chunk.content, end="", flush=True)
#
#   # Multiple calls at once:
#   responses = llm.batch(["q1", "q2", "q3"])
#
#   # Async (for async apps):
#   response = await llm.ainvoke("question")
#
# =============================================================================
