"""
=====================================================
 LLM & AGENTS INTERVIEW PREP — JUNIOR DEV / INTERN
=====================================================

This file has TWO modes:

  1. STUDY GUIDE  — Read through 30 questions with detailed answers.
                    Covers LLMs, RAG, agents, LangChain, and LangGraph.

  2. INTERACTIVE QUIZ — Run this file and answer questions in your terminal.
                         Get scored at the end with feedback.


HOW TO RUN:
  python interview_llms_and_agents.py          (interactive quiz)
  python interview_llms_and_agents.py study    (print study guide)


TOPICS COVERED:
  Round 1 (Easy)     — LLM Fundamentals (tokens, temperature, models)
  Round 2 (Easy-Med) — Prompting & Messages
  Round 3 (Medium)   — RAG Pipeline (embeddings, vectors, retrieval)
  Round 4 (Medium)   — LangChain Concepts (LCEL, chains, runnables)
  Round 5 (Med-Hard) — Agents & Tools (ReAct, tool calling)
  Round 6 (Med-Hard) — LangGraph (state, nodes, edges)
  Round 7 (Hard)     — Architecture & Design Decisions
  Round 8 (Hard)     — Practical Scenarios & Problem Solving
"""

import sys


# =============================================================================
#  ALL QUESTIONS
# =============================================================================

QUESTIONS = [

    # =========================================================================
    # ROUND 1: LLM FUNDAMENTALS (Easy)
    # =========================================================================

    {
        "id": 1,
        "round": "Round 1: LLM Fundamentals",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What is a Large Language Model (LLM)? How does it generate text?",
        "answer": """An LLM is a neural network trained on massive amounts of text data.
It learns patterns in language — grammar, facts, reasoning, style.

HOW IT GENERATES TEXT:
  It predicts the NEXT TOKEN, one at a time.

  Input:  "The capital of France is"
  Model thinks: what word most likely comes next?
  Output: "Paris"

  Then it feeds "The capital of France is Paris" back in and predicts
  the next token again. This is called AUTOREGRESSIVE generation.

  It's essentially a very sophisticated autocomplete.

KEY POINT: LLMs don't "know" things. They've learned statistical
patterns from training data. When they seem to "reason," they're
actually pattern-matching against similar examples they've seen.

EXAMPLES: GPT-4, Claude, Llama, Gemini, Grok

INTERVIEW TIP: Say "It's a next-token predictor trained on large
text corpora." Simple, accurate, shows you understand the core.""",
        "short": ["next token", "predict", "trained", "text", "neural network"],
    },
    {
        "id": 2,
        "round": "Round 1: LLM Fundamentals",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What is a token? Why do LLMs work with tokens instead of words?",
        "answer": """A token is a piece of text — roughly 3/4 of a word on average.

  "Hello world"        = 2 tokens
  "I'm learning LLMs"  = 4 tokens
  "Supercalifragilistic" = multiple tokens (long words get split)

WHY TOKENS, NOT WORDS?
  1. Vocabulary size: There are millions of possible words (including
     typos, names, technical terms). Tokens keep the vocabulary manageable
     (~50,000-100,000 tokens).

  2. Subword handling: "unhappiness" -> "un" + "happiness"
     The model understands parts of words it hasn't seen before.

  3. Multilingual: Works across languages without separate word lists.

WHY IT MATTERS:
  - LLMs have TOKEN LIMITS (context window). GPT-4 = ~128K tokens.
  - You're BILLED per token for API calls.
  - "How many tokens?" determines cost and whether your prompt fits.

ROUGH RULE: 1 token ≈ 4 characters ≈ 0.75 words
  1000 tokens ≈ 750 words ≈ about 1.5 pages of text

INTERVIEW TIP: "Tokens are subword units that let the model handle
any text efficiently. They matter for context limits and cost." """,
        "short": ["subword", "vocabulary", "context", "limit", "cost", "character"],
    },
    {
        "id": 3,
        "round": "Round 1: LLM Fundamentals",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What is temperature? What happens at temperature 0 vs temperature 1?",
        "answer": """Temperature controls RANDOMNESS in the model's output.

  Temperature 0.0 = DETERMINISTIC
    Always picks the most likely next token.
    Same prompt → same response every time.
    Use for: factual Q&A, code generation, data extraction.

  Temperature 0.7 = BALANCED
    Sometimes picks less likely tokens.
    Good mix of coherence and creativity.
    Use for: general chat, content writing.

  Temperature 1.0+ = CREATIVE / RANDOM
    Higher chance of picking unlikely tokens.
    More varied, surprising, sometimes nonsensical.
    Use for: brainstorming, creative writing, poetry.

HOW IT WORKS (simplified):
  The model calculates probabilities for each possible next token.
  "The cat sat on the ___"
    mat: 40%, floor: 25%, roof: 10%, moon: 2%, saxophone: 0.1%

  Temperature 0: Always picks "mat" (highest probability)
  Temperature 0.7: Usually "mat" but sometimes "floor" or "roof"
  Temperature 1.5: Might pick "moon" or even "saxophone"

OTHER SAMPLING PARAMS:
  top_p (nucleus sampling): Only consider tokens within cumulative probability p
  top_k: Only consider the top k most likely tokens
  max_tokens: Maximum length of the response

INTERVIEW TIP: "Temperature 0 for factual tasks, 0.7 for general use,
higher for creativity." Quick, practical answer.""",
        "short": ["randomness", "deterministic", "creative", "probability", "0"],
    },
    {
        "id": 4,
        "round": "Round 1: LLM Fundamentals",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What is a context window? Why does it matter?",
        "answer": """The context window is the maximum number of tokens the model can
process in a single request (input + output combined).

  GPT-4o:    128K tokens (~96K words, ~200 pages)
  Claude:    200K tokens
  Grok:      128K tokens
  Llama 3:   8K-128K tokens (depends on version)

WHY IT MATTERS:
  1. EVERYTHING must fit: your system prompt + conversation history +
     user message + model's response all share the same window.

  2. If you exceed it, the model either:
     - Refuses (API error)
     - Truncates (loses earlier context)
     - Degrades (performs worse on long contexts)

  3. For RAG: you can only send so many document chunks as context.
     More chunks = more info but uses more of the window.

  4. Cost scales with tokens used.

PRACTICAL IMPACT:
  If your chatbot has a 10-message conversation and each message is
  ~200 tokens, that's 2000 tokens of history. Add a system prompt
  (500 tokens) and RAG context (2000 tokens) = 4500 tokens per request.

INTERVIEW TIP: "The context window limits how much information the
model can consider at once. It affects conversation length, RAG
chunk count, and cost." """,
        "short": ["maximum", "tokens", "input", "output", "limit", "conversation"],
    },
    {
        "id": 5,
        "round": "Round 1: LLM Fundamentals",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What is the difference between fine-tuning and prompting? When use each?",
        "answer": """PROMPTING — give the model instructions at runtime.
  No training. You just write a good prompt.
  "You are a helpful assistant that speaks like a pirate."

  Pros: Instant, no data needed, easy to iterate
  Cons: Limited by context window, can be inconsistent

FINE-TUNING — retrain the model on your specific data.
  You provide examples, the model updates its weights.

  Pros: Consistent style/behavior, works without long prompts
  Cons: Expensive, needs training data, takes time, can overfit

RAG (Retrieval-Augmented Generation) — a third option!
  Don't retrain, don't put everything in the prompt.
  Instead: retrieve relevant info at runtime and add it to the prompt.

  Pros: Up-to-date data, no training, cost-effective
  Cons: Depends on retrieval quality, adds latency

DECISION FRAMEWORK:
  Need the model to KNOW specific facts?       -> RAG
  Need the model to BEHAVE a certain way?       -> Fine-tuning
  Need a quick, flexible solution?              -> Prompting
  Need all three?                               -> Prompting + RAG (most common)

INTERVIEW TIP: "Start with prompting, add RAG for knowledge, only
fine-tune if you need consistent style or behavior." Shows pragmatism.""",
        "short": ["prompt", "fine-tune", "RAG", "retrain", "data", "retrieve"],
    },

    # =========================================================================
    # ROUND 2: PROMPTING & MESSAGES (Easy-Medium)
    # =========================================================================

    {
        "id": 6,
        "round": "Round 2: Prompting & Messages",
        "difficulty": "Easy-Medium",
        "type": "Conceptual",
        "question": "What are the different message types in a chat model (system, human, AI)?",
        "answer": """Chat models use a CONVERSATION format with message roles:

  SYSTEM MESSAGE — sets the model's behavior/persona.
    "You are a Python expert. Be concise. Use examples."
    Sent once at the start. The model follows these instructions
    throughout the conversation.

  HUMAN MESSAGE (user) — what the user says.
    "How do I read a file in Python?"

  AI MESSAGE (assistant) — the model's response.
    "Use open() with a with statement: ..."

A typical API call looks like:
  messages = [
      SystemMessage("You are a helpful coding assistant."),
      HumanMessage("What is a list comprehension?"),
      AIMessage("A list comprehension is..."),          # previous response
      HumanMessage("Can you give me an example?"),      # new question
  ]

The model sees the FULL conversation each time. It doesn't have
memory between API calls — YOU manage the history.

IN LANGCHAIN:
  from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

INTERVIEW TIP: Mention that the model is STATELESS — every call
sends the full conversation. "Memory" is just appending messages.""",
        "short": ["system", "human", "AI", "role", "conversation", "stateless"],
    },
    {
        "id": 7,
        "round": "Round 2: Prompting & Messages",
        "difficulty": "Easy-Medium",
        "type": "Conceptual",
        "question": "What is prompt engineering? What makes a good prompt?",
        "answer": """Prompt engineering is crafting your input to get the best output
from an LLM. The same question asked differently gets very different results.

GOOD PROMPT PRINCIPLES:

  1. BE SPECIFIC — don't say "help me with code", say "write a Python
     function that takes a list of integers and returns the sum of evens."

  2. GIVE CONTEXT — "You are a senior Python developer reviewing code
     for a production web application."

  3. PROVIDE EXAMPLES (few-shot prompting):
     "Convert these to title case:
      'hello world' -> 'Hello World'
      'foo bar baz' -> 'Foo Bar Baz'
      'python is great' -> ?"

  4. SPECIFY FORMAT — "Return your answer as JSON with keys: name, age, email"

  5. CHAIN OF THOUGHT — "Think step by step before answering."
     This dramatically improves reasoning on complex problems.

PROMPTING TECHNIQUES:
  Zero-shot:  Just ask the question (no examples)
  Few-shot:   Give 2-3 examples first, then ask
  Chain-of-thought: "Let's think step by step"
  Role-based:  "You are an expert in..."

INTERVIEW TIP: Mention few-shot prompting and chain-of-thought
by name. These are the two techniques interviewers expect you to know.""",
        "short": ["specific", "examples", "few-shot", "chain-of-thought", "context", "format"],
    },
    {
        "id": 8,
        "round": "Round 2: Prompting & Messages",
        "difficulty": "Easy-Medium",
        "type": "Conceptual",
        "question": "What is streaming? Why would you use it instead of waiting for the full response?",
        "answer": """STREAMING means receiving the model's response TOKEN BY TOKEN as it's
being generated, instead of waiting for the entire response to finish.

WITHOUT STREAMING:
  User asks question -> waits 5 seconds -> gets entire response at once
  (Bad UX — user stares at a loading spinner)

WITH STREAMING:
  User asks question -> tokens appear one by one -> feels instant
  (Good UX — like watching someone type, user reads as it generates)

IN LANGCHAIN:
  # Without streaming (returns complete response):
  result = chain.invoke({"question": "What is Python?"})

  # With streaming (yields chunks):
  for chunk in chain.stream({"question": "What is Python?"}):
      print(chunk, end="")   # Prints token by token

STREAMING RETURNS AIMessageChunk objects, not AIMessage.
Each chunk contains a small piece of the response.

WHY USE IT:
  1. Better UX — perceived latency drops dramatically
  2. Time to first token — user sees something almost immediately
  3. Long responses — user can start reading before it's done
  4. Can cancel early — if the response is going in the wrong direction

INTERVIEW TIP: "Streaming improves perceived latency by showing
tokens as they're generated. It uses .stream() instead of .invoke()
and returns AIMessageChunk objects." """,
        "short": ["token by token", "chunk", "latency", "UX", "stream", "invoke"],
    },

    # =========================================================================
    # ROUND 3: RAG PIPELINE (Medium)
    # =========================================================================

    {
        "id": 9,
        "round": "Round 3: RAG Pipeline",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is RAG? Walk me through the full pipeline.",
        "answer": """RAG = Retrieval-Augmented Generation

Instead of the LLM relying only on its training data, you RETRIEVE
relevant information and ADD it to the prompt as context.

THE FULL PIPELINE (2 phases):

INDEXING PHASE (done once, ahead of time):
  1. LOAD — Load your documents (PDFs, web pages, databases)
     TextLoader, WebBaseLoader, CSVLoader

  2. SPLIT — Break documents into small chunks (~500-1000 chars)
     RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
     Why? LLMs have context limits. Small chunks = precise retrieval.

  3. EMBED — Convert each chunk into a vector (list of numbers)
     HuggingFaceEmbeddings or OpenAIEmbeddings
     Similar meaning = similar vectors.

  4. STORE — Save vectors in a vector database
     ChromaDB, Pinecone, Weaviate, FAISS

QUERY PHASE (every time a user asks a question):
  5. EMBED the question — same embedding model as step 3

  6. RETRIEVE — find the most similar chunks (semantic search)
     Vector store compares question vector to all chunk vectors.
     Returns top-k most relevant chunks.

  7. GENERATE — send the chunks + question to the LLM
     "Based on this context: {chunks}, answer: {question}"

WHY RAG OVER FINE-TUNING?
  - No retraining needed
  - Data can be updated instantly
  - Cheaper and faster to set up
  - Sources are traceable (you know which chunk the answer came from)

INTERVIEW TIP: Know the 7 steps cold. Draw it on a whiteboard if asked.
Load → Split → Embed → Store → (query) Embed → Retrieve → Generate.""",
        "short": ["retrieval", "augmented", "generation", "embed", "vector", "chunk", "retrieve"],
    },
    {
        "id": 10,
        "round": "Round 3: RAG Pipeline",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What are embeddings? What is cosine similarity?",
        "answer": """EMBEDDINGS convert text into a list of numbers (a vector) that
captures the MEANING of the text.

  "How do I cook pasta?"         -> [0.2, 0.8, 0.1, 0.5, ...]
  "What's the recipe for noodles?" -> [0.21, 0.79, 0.12, 0.48, ...]
  "Explain quantum physics"      -> [0.9, 0.1, 0.7, 0.3, ...]

Similar meaning = similar numbers. Different meaning = different numbers.

This is what makes SEMANTIC SEARCH possible:
  Keyword search: "cook pasta" won't match "noodle recipe"
  Semantic search: "cook pasta" WILL match "noodle recipe" (similar meaning!)

COSINE SIMILARITY measures the angle between two vectors:
  1.0  = identical direction (same meaning)
  0.0  = perpendicular (completely unrelated)
  -1.0 = opposite direction (rare in practice)

EMBEDDING MODELS:
  Cloud (paid):  OpenAI text-embedding-3-small (1536 dims)
  Local (free):  HuggingFace all-MiniLM-L6-v2 (384 dims)

CRITICAL RULE:
  You MUST use the SAME embedding model for documents AND queries.
  You can't embed docs with OpenAI and search with HuggingFace —
  the vectors would be in completely different spaces.

INTERVIEW TIP: "Embeddings capture semantic meaning as vectors.
Cosine similarity measures how close two vectors are. This enables
finding relevant documents by meaning, not just keyword matching." """,
        "short": ["vector", "meaning", "similar", "cosine", "semantic", "numbers"],
    },
    {
        "id": 11,
        "round": "Round 3: RAG Pipeline",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "Why do we split documents into chunks? What is chunk_size and chunk_overlap?",
        "answer": """WHY CHUNK?
  1. Context window limit — you can't send a 100-page PDF to an LLM.
  2. Precision — smaller chunks mean more precise retrieval.
     If you search for "how to cook pasta" and your chunk is an entire
     chapter, you get lots of irrelevant text. If it's a paragraph,
     you get exactly the relevant part.
  3. Embedding quality — embedding models work better on shorter text.

CHUNK_SIZE — maximum characters per chunk.
  chunk_size=500 means each chunk is at most 500 characters.

  Too small (100): chunks lose context, fragments of sentences
  Too big (5000): chunks are too broad, retrieval is imprecise
  Sweet spot: 500-1000 for most use cases

CHUNK_OVERLAP — how much consecutive chunks share.
  chunk_overlap=50 means the last 50 characters of chunk N
  are also the first 50 characters of chunk N+1.

  Why? So you don't cut a sentence in half. The overlap ensures
  information at chunk boundaries isn't lost.

  "The quick brown fox jumps over the lazy dog."
  Without overlap: ["The quick brown fo", "x jumps over the la", "zy dog."]
  With overlap:    ["The quick brown fox", "fox jumps over the", "the lazy dog."]

SPLITTER TYPES:
  RecursiveCharacterTextSplitter — tries to split on paragraphs, then
  sentences, then words. Keeps text natural. This is the DEFAULT choice.

INTERVIEW TIP: "I use RecursiveCharacterTextSplitter with ~500 chunk
size and ~50 overlap. It preserves sentence boundaries and ensures
no information is lost at chunk edges." """,
        "short": ["chunk_size", "overlap", "precision", "context", "split", "boundary"],
    },
    {
        "id": 12,
        "round": "Round 3: RAG Pipeline",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is a vector store? How does retrieval work?",
        "answer": """A vector store is a DATABASE optimized for storing and searching
vectors (embeddings). It's like a regular database but instead of
SQL queries, you search by SIMILARITY.

HOW IT WORKS:
  1. You store document chunks with their embedding vectors
  2. When a user asks a question, you embed the question
  3. The vector store finds the k vectors closest to the question
  4. Returns the corresponding text chunks

POPULAR VECTOR STORES:
  ChromaDB    — lightweight, local, great for learning (what we use)
  FAISS       — Facebook's library, very fast, local
  Pinecone    — cloud-hosted, managed, scales well
  Weaviate    — cloud or self-hosted, feature-rich
  Qdrant      — open source, high performance

IN LANGCHAIN:
  # Store documents:
  vectorstore = Chroma.from_documents(chunks, embeddings)

  # Search:
  results = vectorstore.similarity_search("my question", k=3)
  # Returns the 3 most similar chunks

  # As a retriever (for use in chains):
  retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

RETRIEVER vs VECTOR STORE:
  Vector store = the database itself
  Retriever = a LangChain interface that wraps the vector store
  retriever.invoke("my question") returns relevant documents

INTERVIEW TIP: "A vector store indexes embeddings for fast similarity
search. In LangChain, you convert it to a retriever with .as_retriever()
to plug it into a RAG chain." """,
        "short": ["vector", "database", "similarity", "retriever", "search", "Chroma"],
    },

    # =========================================================================
    # ROUND 4: LANGCHAIN CONCEPTS (Medium)
    # =========================================================================

    {
        "id": 13,
        "round": "Round 4: LangChain",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is LangChain? What problem does it solve?",
        "answer": """LangChain is a FRAMEWORK for building applications powered by LLMs.

THE PROBLEM IT SOLVES:
  Without LangChain, building an LLM app means:
  - Raw API calls to OpenAI/Anthropic/etc.
  - Manually managing prompts, memory, context
  - Writing your own document loading, splitting, embedding code
  - Building chains of operations from scratch

  LangChain gives you BUILDING BLOCKS that snap together:
  - Prompt templates
  - LLM wrappers (same interface for any provider)
  - Output parsers
  - Document loaders
  - Text splitters
  - Vector stores
  - Chains (sequence of operations)
  - Agents (LLM decides what to do)

KEY CONCEPTS:
  1. LCEL (LangChain Expression Language) — pipe syntax for chains:
     chain = prompt | llm | parser

  2. Runnables — everything in LangChain is a Runnable with:
     .invoke()  — run once, get full result
     .stream()  — get results token by token
     .batch()   — run on multiple inputs in parallel

  3. Provider-agnostic — swap OpenAI for Claude or Llama with one line

INTERVIEW TIP: "LangChain provides modular building blocks for LLM
apps. Its pipe syntax lets you chain operations together, and everything
is a Runnable with invoke/stream/batch." """,
        "short": ["framework", "building blocks", "chain", "Runnable", "LCEL", "pipe"],
    },
    {
        "id": 14,
        "round": "Round 4: LangChain",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is LCEL? How does the pipe syntax work?",
        "answer": """LCEL = LangChain Expression Language

It's a way to chain operations using the PIPE operator (|):

  chain = prompt | llm | output_parser

This is equivalent to:
  result = output_parser.invoke(llm.invoke(prompt.invoke(input)))

But the pipe syntax is cleaner and gives you streaming, batching,
and async for free.

HOW IT WORKS:
  Each component is a "Runnable" with an invoke() method.
  The pipe (|) connects them: output of one becomes input of the next.

  Step 1: prompt.invoke({"topic": "Python"})
           -> "Tell me a joke about Python"

  Step 2: llm.invoke("Tell me a joke about Python")
           -> AIMessage("Why do Python programmers...")

  Step 3: parser.invoke(AIMessage(...))
           -> "Why do Python programmers..."

COMPOSABILITY:
  You can build complex chains from simple pieces:

  # Simple:
  chain = prompt | llm | parser

  # With retrieval:
  chain = (
      {"context": retriever, "question": RunnablePassthrough()}
      | prompt
      | llm
      | parser
  )

  # Parallel:
  chain = RunnableParallel(
      joke=joke_prompt | llm | parser,
      poem=poem_prompt | llm | parser,
  )

INTERVIEW TIP: "LCEL uses the pipe operator to chain Runnables.
Data flows left to right. Each component transforms the output for
the next one. It's like Unix pipes for LLM operations." """,
        "short": ["pipe", "chain", "Runnable", "invoke", "output", "input", "operator"],
    },
    {
        "id": 15,
        "round": "Round 4: LangChain",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is an output parser? Why do you need one?",
        "answer": """An output parser converts the LLM's response into a structured format.

THE PROBLEM:
  LLMs return RAW TEXT (as AIMessage objects).
  You often need structured data: JSON, a list, a Python object.

  Without a parser:
    result = llm.invoke("List 3 fruits")
    # AIMessage(content="1. Apple\\n2. Banana\\n3. Cherry")
    # Now you have to manually parse this string... fragile!

  With a parser:
    result = chain.invoke("List 3 fruits")
    # ["Apple", "Banana", "Cherry"]  — clean Python list!

COMMON PARSERS:

  StrOutputParser()
    Extracts just the text string from AIMessage.
    AIMessage(content="Hello") -> "Hello"
    Most common, used in almost every chain.

  JsonOutputParser()
    Parses the LLM's response as JSON.
    Adds format instructions to the prompt automatically.

  PydanticOutputParser(pydantic_object=MyModel)
    Parses into a typed Python object.
    class Joke(BaseModel):
        setup: str
        punchline: str
    Result: Joke(setup="...", punchline="...")

  .with_structured_output(MyModel)
    Modern approach — uses the LLM's built-in JSON mode.
    Most reliable, recommended for production.

INTERVIEW TIP: "Output parsers convert raw LLM text into structured
data. I'd use StrOutputParser for text, and .with_structured_output()
for typed objects like Pydantic models." """,
        "short": ["structured", "parse", "JSON", "AIMessage", "string", "Pydantic"],
    },

    # =========================================================================
    # ROUND 5: AGENTS & TOOLS (Medium-Hard)
    # =========================================================================

    {
        "id": 16,
        "round": "Round 5: Agents & Tools",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is the difference between a chain and an agent?",
        "answer": """CHAIN — a fixed sequence of steps. The path is predetermined.
  prompt -> LLM -> parser
  Always runs the same steps in the same order.

  Like a recipe: Step 1, Step 2, Step 3. Always.

AGENT — the LLM DECIDES what to do at each step.
  The LLM looks at the task, chooses a tool, observes the result,
  then decides what to do next. The path is DYNAMIC.

  Like a chef: looks at what's available, decides what to cook,
  tastes it, adjusts seasoning, serves when ready.

EXAMPLE — answering "What's the weather in Paris?":

  Chain approach (fixed):
    1. Always call weather API
    2. Always format result
    3. Always return

  Agent approach (dynamic):
    1. LLM reads question, thinks: "I need weather data"
    2. LLM chooses: call weather_tool("Paris")
    3. LLM observes result: {"temp": 20, "condition": "sunny"}
    4. LLM thinks: "I have the answer now"
    5. LLM responds: "It's 20°C and sunny in Paris!"

    But if the question was "Tell me a joke", the agent would
    skip the weather tool entirely and just respond.

WHEN TO USE:
  Chain: simple, predictable tasks (summarize, translate, format)
  Agent: complex tasks that need tools, decisions, or multiple steps

INTERVIEW TIP: "A chain is a fixed pipeline. An agent uses the LLM
to dynamically choose which tools to call and in what order." """,
        "short": ["fixed", "dynamic", "decides", "tool", "choose", "step"],
    },
    {
        "id": 17,
        "round": "Round 5: Agents & Tools",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is the ReAct pattern? How does an agent use it?",
        "answer": """ReAct = Reasoning + Acting

The agent follows a loop:
  1. REASON — think about what to do next
  2. ACT — call a tool
  3. OBSERVE — look at the tool's result
  4. Repeat until the task is done

EXAMPLE — "What's the population of the capital of France?"

  THOUGHT: I need to find the capital of France first.
  ACTION: search("capital of France")
  OBSERVATION: Paris is the capital of France.

  THOUGHT: Now I need the population of Paris.
  ACTION: search("population of Paris")
  OBSERVATION: Paris has approximately 2.1 million people.

  THOUGHT: I have the answer now.
  FINAL ANSWER: The population of Paris, the capital of France,
  is approximately 2.1 million people.

The key insight: the LLM REASONS before acting. It doesn't just
blindly call tools — it thinks about what information it needs
and which tool would provide it.

IN LANGCHAIN:
  from langgraph.prebuilt import create_react_agent
  agent = create_react_agent(llm, tools=[search, calculator])

INTERVIEW TIP: "ReAct is a loop of Reason-Act-Observe. The LLM
thinks about what it needs, calls a tool, checks the result, and
repeats until it can answer. It's the standard agent pattern." """,
        "short": ["reason", "act", "observe", "loop", "think", "tool"],
    },
    {
        "id": 18,
        "round": "Round 5: Agents & Tools",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is a tool in the context of agents? How do you create one?",
        "answer": """A TOOL is a function that an agent can call to interact with the
outside world. The LLM can't browse the web, run code, or query
databases on its own — tools give it these abilities.

COMMON TOOLS:
  - Web search (look up current information)
  - Calculator (do math)
  - Database query (retrieve data)
  - API calls (weather, stock prices, etc.)
  - Code execution (run Python/JS)
  - File operations (read/write files)

HOW TO CREATE A TOOL IN LANGCHAIN:

  from langchain_core.tools import tool

  @tool
  def get_weather(city: str) -> str:
      \"\"\"Get the current weather for a city.\"\"\"
      # API call here...
      return f"It's 72°F and sunny in {city}"

THE @tool DECORATOR:
  1. The function name becomes the tool name
  2. The docstring becomes the tool DESCRIPTION (critical! The LLM
     reads this to decide when to use the tool)
  3. The type hints become the tool's input schema
  4. The LLM sees: name, description, and parameters — then decides
     whether to call it

TOOL CALLING FLOW:
  1. You give the agent a list of tools
  2. User asks a question
  3. LLM looks at available tools and their descriptions
  4. LLM decides which tool to call (if any) and with what arguments
  5. Your code executes the tool
  6. Result goes back to the LLM
  7. LLM either calls another tool or gives a final answer

INTERVIEW TIP: "Tools are functions the LLM can invoke. The docstring
is crucial — it's what the LLM reads to decide when to use the tool.
I use the @tool decorator in LangChain to define them." """,
        "short": ["function", "call", "decorator", "@tool", "docstring", "description"],
    },
    {
        "id": 19,
        "round": "Round 5: Agents & Tools",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is tool calling? How is it different from the LLM just generating text?",
        "answer": """Normally, an LLM generates TEXT. With tool calling, the LLM generates
a STRUCTURED FUNCTION CALL instead.

NORMAL LLM:
  Input:  "What's 234 * 567?"
  Output: "234 * 567 = 132,678"  (might be wrong! LLMs are bad at math)

WITH TOOL CALLING:
  Input:  "What's 234 * 567?"
  Output: {
      "tool": "calculator",
      "arguments": {"expression": "234 * 567"}
  }
  Your code runs the calculator: 234 * 567 = 132678 (correct!)
  That result goes back to the LLM.
  LLM final response: "234 * 567 = 132,678"

KEY INSIGHT:
  The LLM doesn't EXECUTE the tool. It decides WHICH tool to call
  and with WHAT arguments. Your code handles execution.

  LLM's job:  "I should call calculator with '234 * 567'"
  Your job:   Actually run the calculation
  LLM's job:  Format the result for the user

This is a STRUCTURED OUTPUT from the LLM — it returns JSON with
the tool name and arguments, not free-form text.

Modern LLMs (GPT-4, Claude, Grok) have built-in tool calling support.
They've been trained to output tool calls in a specific format.

INTERVIEW TIP: "Tool calling lets the LLM output structured function
calls instead of text. The LLM decides what to call, our code executes
it, and the result goes back to the LLM." """,
        "short": ["structured", "function call", "execute", "arguments", "JSON", "decides"],
    },

    # =========================================================================
    # ROUND 6: LANGGRAPH (Medium-Hard)
    # =========================================================================

    {
        "id": 20,
        "round": "Round 6: LangGraph",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is LangGraph? How is it different from LangChain?",
        "answer": """LANGCHAIN = building blocks (prompts, LLMs, parsers, tools)
LANGGRAPH = orchestration framework built ON TOP of LangChain

Think of it like:
  LangChain = the LEGO bricks
  LangGraph = the instructions for building complex structures

LANGCHAIN gives you chains (fixed pipelines):
  prompt -> LLM -> parser (always the same path)

LANGGRAPH gives you GRAPHS (dynamic workflows):
  - Nodes (steps/functions)
  - Edges (connections between steps)
  - Conditional edges (if/else routing)
  - Loops (retry, iterate, self-correct)
  - State (shared data that persists across steps)

WHY LANGGRAPH?
  Chains can't do:
  - Loops (try again if the answer is bad)
  - Conditional routing (go to A if X, go to B if Y)
  - Multi-agent workflows (agent 1 writes, agent 2 reviews)
  - Human-in-the-loop (pause, ask human, continue)

  LangGraph handles all of these.

EXAMPLE:
  Chain:   question -> LLM -> answer (one shot)
  Graph:   question -> LLM -> check quality -> if bad, retry -> answer

INTERVIEW TIP: "LangGraph adds loops, branching, and state management
on top of LangChain. I use it when I need agents with conditional
logic, retries, or multi-step workflows." """,
        "short": ["graph", "nodes", "edges", "loops", "state", "conditional", "orchestration"],
    },
    {
        "id": 21,
        "round": "Round 6: LangGraph",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is state in LangGraph? Why is it important?",
        "answer": """STATE is a shared data object that flows through the entire graph.
Every node can read from it and write to it.

  class MyState(TypedDict):
      question: str
      context: list[str]
      answer: str
      retry_count: int

It's like a CLIPBOARD that gets passed from node to node:
  Node 1 (retrieve): reads question, writes context
  Node 2 (generate): reads question + context, writes answer
  Node 3 (evaluate): reads answer, updates retry_count

WHY IT MATTERS:
  1. Nodes communicate through state (not direct function calls)
  2. State persists across the entire workflow
  3. You can inspect state at any point for debugging
  4. With checkpointing, state can be SAVED and RESUMED

REDUCERS — how state updates are combined:
  By default, new values REPLACE old values.
  With Annotated[list, operator.add], new values are APPENDED.

  # Replace (default):
  state["answer"] = "new answer"   # Overwrites the old answer

  # Append (with reducer):
  state["messages"] = [new_message]  # Appends to existing list

  MessagesState is a pre-built state with an append reducer on
  the "messages" key — perfect for chatbot conversations.

INTERVIEW TIP: "State is a TypedDict shared across all nodes.
Nodes read inputs and write outputs to state. Reducers control
whether updates replace or append." """,
        "short": ["TypedDict", "shared", "nodes", "read", "write", "reducer", "persist"],
    },
    {
        "id": 22,
        "round": "Round 6: LangGraph",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What are nodes and edges in LangGraph? What is a conditional edge?",
        "answer": """NODES are functions that do work. Each node:
  - Takes state as input
  - Does something (call LLM, process data, call API)
  - Returns updates to state

  def retrieve(state: MyState) -> dict:
      docs = retriever.invoke(state["question"])
      return {"context": docs}

EDGES connect nodes and define the flow:
  graph.add_edge("retrieve", "generate")  # After retrieve, go to generate

CONDITIONAL EDGES let you branch based on state:
  def should_retry(state: MyState) -> str:
      if state["quality"] == "good":
          return "end"        # Go to END node
      return "generate"       # Go back to generate (retry!)

  graph.add_conditional_edges("evaluate", should_retry)

SPECIAL NODES:
  START — where the graph begins
  END   — where the graph finishes

  graph.add_edge(START, "retrieve")    # Start at retrieve
  graph.add_edge("generate", END)      # End after generate

BUILDING A GRAPH:
  graph = StateGraph(MyState)
  graph.add_node("retrieve", retrieve_fn)
  graph.add_node("generate", generate_fn)
  graph.add_edge(START, "retrieve")
  graph.add_edge("retrieve", "generate")
  graph.add_edge("generate", END)
  app = graph.compile()

INTERVIEW TIP: "Nodes are functions, edges define flow. Conditional
edges enable branching and loops — the LLM can retry, route to
different paths, or loop until quality is met." """,
        "short": ["node", "edge", "conditional", "function", "branch", "START", "END"],
    },
    {
        "id": 23,
        "round": "Round 6: LangGraph",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is human-in-the-loop? Why would you use it?",
        "answer": """Human-in-the-loop means the agent PAUSES and waits for a human
to approve, modify, or provide input before continuing.

WHY?
  You don't want an agent to:
  - Send an email without review
  - Delete files without confirmation
  - Make a purchase without approval
  - Execute code that might be dangerous

  Human-in-the-loop adds a safety checkpoint.

HOW IT WORKS IN LANGGRAPH:
  1. The graph hits an `interrupt()` call
  2. Execution PAUSES and returns to the user
  3. The user reviews and provides input (approve/reject/modify)
  4. The graph RESUMES from where it paused

  from langgraph.types import interrupt, Command

  def send_email(state):
      # Pause and ask the human
      approval = interrupt({
          "question": "Send this email?",
          "draft": state["email_draft"]
      })
      if approval == "yes":
          actually_send_email(state["email_draft"])

CHECKPOINTING:
  For interrupt to work, you need a checkpointer (saves state):
  graph.compile(checkpointer=MemorySaver())

  The checkpointer saves the entire state so the graph can resume
  exactly where it left off.

THREADS:
  Each conversation gets a thread_id so multiple users can have
  independent sessions.

INTERVIEW TIP: "Human-in-the-loop uses interrupt() to pause the
agent at critical points. The state is saved via checkpointing
so it can resume after human approval." """,
        "short": ["interrupt", "pause", "approve", "checkpoint", "resume", "safety"],
    },

    # =========================================================================
    # ROUND 7: ARCHITECTURE & DESIGN (Hard)
    # =========================================================================

    {
        "id": 24,
        "round": "Round 7: Architecture & Design",
        "difficulty": "Hard",
        "type": "Conceptual",
        "question": "What are the common failure modes of RAG? How do you fix them?",
        "answer": """RAG FAILURE MODES:

1. RETRIEVAL FAILS — wrong chunks are retrieved
   Symptoms: Answer is wrong or says "I don't know" when the info exists
   Fixes:
   - Better chunking (smaller chunks, more overlap)
   - Better embeddings (try a different model)
   - Rewrite the query (LLM rephrases the question for better search)
   - Hybrid search (combine semantic + keyword search)

2. CONTEXT IS IRRELEVANT — chunks are retrieved but not useful
   Symptoms: Answer ignores the context or hallucinates
   Fixes:
   - Increase k (retrieve more chunks)
   - Add a relevance filter (score threshold)
   - Re-rank results (use a cross-encoder to re-score)

3. LLM IGNORES CONTEXT — LLM uses its own knowledge instead
   Symptoms: Answer contradicts the provided documents
   Fixes:
   - Stronger system prompt: "ONLY use the provided context"
   - Lower temperature (less creative = more faithful)
   - Explicitly say "If the context doesn't contain the answer, say so"

4. LOST IN THE MIDDLE — LLM pays less attention to middle chunks
   Symptoms: Misses info that's in the middle of the context
   Fixes:
   - Put most relevant chunks first and last
   - Use fewer, more relevant chunks
   - Summarize chunks before sending

5. HALLUCINATION — LLM makes up information
   Fixes:
   - Ask for citations/sources
   - Chain-of-thought: "Quote the relevant passage, then answer"
   - Post-processing: verify answer against source chunks

INTERVIEW TIP: Know at least 3 failure modes and their fixes.
"Retrieval quality is the #1 factor — if you retrieve the wrong
chunks, the LLM can't give a good answer." """,
        "short": ["retrieval", "hallucination", "chunk", "relevance", "context", "re-rank"],
    },
    {
        "id": 25,
        "round": "Round 7: Architecture & Design",
        "difficulty": "Hard",
        "type": "Conceptual",
        "question": "When would you use a multi-agent system instead of a single agent?",
        "answer": """SINGLE AGENT — one LLM handles everything.
  Good for: simple tasks, one area of expertise, quick interactions.

MULTI-AGENT — multiple specialized LLMs collaborate.
  Good for: complex workflows where different steps need different skills.

USE MULTI-AGENT WHEN:

  1. DIFFERENT EXPERTISE NEEDED:
     Writer agent (creative, high temperature)
     Editor agent (critical, low temperature)
     Fact-checker agent (has search tools)

  2. QUALITY THROUGH REVIEW:
     Agent 1 generates code
     Agent 2 reviews for bugs
     Agent 1 fixes based on feedback
     Loop until Agent 2 approves

  3. COMPLEX PIPELINES:
     Research agent -> Outline agent -> Writing agent -> Review agent

  4. SEPARATION OF CONCERNS:
     Router agent (decides which specialist to call)
     SQL agent (handles database queries)
     Search agent (handles web searches)
     Math agent (handles calculations)

PATTERNS:
  - Supervisor: one agent delegates to specialists
  - Pipeline: agents in sequence (output -> input)
  - Debate: agents argue, then consensus
  - Writer-reviewer: generate -> review -> revise loop

IN LANGGRAPH:
  Each agent is a node. Edges connect them.
  Conditional edges route to the right specialist.

INTERVIEW TIP: "I'd use multi-agent when tasks need different skills
or when quality benefits from a generate-review loop. Each agent
is a node in a LangGraph with conditional routing between them." """,
        "short": ["specialist", "collaborate", "review", "supervisor", "route", "loop"],
    },
    {
        "id": 26,
        "round": "Round 7: Architecture & Design",
        "difficulty": "Hard",
        "type": "Conceptual",
        "question": "How would you evaluate an LLM application? What metrics would you use?",
        "answer": """EVALUATING LLM APPS IS HARD because outputs are subjective text.
But there are established approaches:

FOR RAG:
  1. Retrieval quality:
     - Precision: What % of retrieved chunks are relevant?
     - Recall: What % of relevant chunks were retrieved?
     - MRR (Mean Reciprocal Rank): Is the best chunk ranked first?

  2. Generation quality:
     - Faithfulness: Does the answer match the retrieved context?
       (No hallucination)
     - Relevance: Does the answer actually address the question?
     - Completeness: Does the answer cover all relevant info?

FOR AGENTS:
  - Task completion rate: Did it finish the task?
  - Tool use accuracy: Did it call the right tools?
  - Efficiency: How many steps did it take?
  - Error recovery: Did it handle failures gracefully?

EVALUATION METHODS:
  1. Human evaluation — gold standard but slow and expensive
  2. LLM-as-judge — use GPT-4/Claude to rate outputs (fast, scalable)
  3. Reference-based — compare against known correct answers
     BLEU, ROUGE scores (for summarization)
  4. Automated test suites — predefined question-answer pairs

TOOLS:
  - RAGAS (RAG Assessment) — popular framework for RAG evaluation
  - LangSmith — LangChain's evaluation/tracing platform
  - Custom eval scripts with LLM-as-judge

INTERVIEW TIP: "I'd use faithfulness and relevance for RAG quality,
measured with LLM-as-judge and a test set of question-answer pairs.
For agents, task completion rate and tool accuracy." """,
        "short": ["faithfulness", "relevance", "precision", "recall", "evaluation", "metrics"],
    },

    # =========================================================================
    # ROUND 8: PRACTICAL SCENARIOS (Hard)
    # =========================================================================

    {
        "id": 27,
        "round": "Round 8: Practical Scenarios",
        "difficulty": "Hard",
        "type": "Scenario",
        "question": "You're building a chatbot for a company's internal docs. Walk me through your approach.",
        "answer": """I'd build a RAG chatbot. Here's my step-by-step approach:

1. DATA INGESTION:
   - Identify sources: Confluence pages, PDFs, Google Docs, wikis
   - Use LangChain document loaders for each source type
   - Schedule regular re-indexing (cron job or webhook)

2. CHUNKING STRATEGY:
   - RecursiveCharacterTextSplitter, chunk_size=500, overlap=50
   - Preserve metadata: source URL, document title, date
   - This metadata lets users click through to the original doc

3. EMBEDDING & STORAGE:
   - HuggingFace embeddings for cost savings (or OpenAI for quality)
   - Vector store: ChromaDB for prototype, Pinecone for production
   - Index chunks with their metadata

4. RETRIEVAL:
   - Retrieve top 3-5 chunks per query
   - Consider hybrid search (semantic + keyword) for better recall
   - Add a relevance threshold to filter out low-quality matches

5. GENERATION:
   - System prompt: "Answer based on the provided context. If the
     context doesn't contain the answer, say you don't know."
   - Include source citations in the response
   - Use streaming for better UX

6. CONVERSATION MEMORY:
   - Store chat history so users can ask follow-up questions
   - Use MessagesState or a message history wrapper

7. EVALUATION & ITERATION:
   - Collect user feedback (thumbs up/down)
   - Build a test set of common questions
   - Monitor retrieval quality and answer faithfulness

INTERVIEW TIP: Walk through this systematically. Mention metadata,
citations, and evaluation — it shows production-level thinking.""",
        "short": ["RAG", "chunk", "embed", "vector", "retriever", "metadata", "citation"],
    },
    {
        "id": 28,
        "round": "Round 8: Practical Scenarios",
        "difficulty": "Hard",
        "type": "Scenario",
        "question": "Your RAG system is returning wrong answers. How do you debug it?",
        "answer": """SYSTEMATIC DEBUGGING — check each stage of the pipeline:

STEP 1: CHECK RETRIEVAL FIRST (most common problem)
  - Run the query against the vector store manually
  - Look at the retrieved chunks: are they relevant?
  - If chunks are wrong, the LLM can't give a good answer.

  Fix retrieval:
  - Try different chunk sizes
  - Try a different embedding model
  - Add keyword search alongside semantic search
  - Rephrase the query (query expansion)

STEP 2: CHECK THE CHUNKS THEMSELVES
  - Open the vector store, look at what was indexed
  - Are the documents actually there?
  - Was the text extracted correctly? (PDFs can be messy)
  - Are chunks too big (noisy) or too small (missing context)?

STEP 3: CHECK THE PROMPT
  - Print the full prompt being sent to the LLM
  - Is the context being inserted correctly?
  - Is the system prompt clear enough?
  - Try: "ONLY use the provided context. If you can't find the
    answer in the context, say 'I don't have that information.'"

STEP 4: CHECK THE LLM
  - Is temperature too high? (hallucination risk)
  - Is the model capable enough? (try a bigger model)
  - Does the model's context window fit all your chunks?

STEP 5: USE TRACING
  - LangSmith or similar tool to trace every step
  - See exactly what was retrieved, what was sent, what was returned
  - Identify the bottleneck

DEBUGGING ORDER: Retrieval -> Chunks -> Prompt -> LLM

INTERVIEW TIP: "I'd start by checking retrieval quality — that's the
root cause 80% of the time. Print the retrieved chunks, see if they're
relevant, and fix chunking or search if not." """,
        "short": ["retrieval", "chunks", "prompt", "debug", "tracing", "LangSmith"],
    },
    {
        "id": 29,
        "round": "Round 8: Practical Scenarios",
        "difficulty": "Hard",
        "type": "Scenario",
        "question": "How would you handle hallucination in an LLM application?",
        "answer": """HALLUCINATION = the model confidently states something that's wrong
or not supported by the provided context.

PREVENTION STRATEGIES:

1. STRONG SYSTEM PROMPT:
   "Only answer based on the provided context. If the context
   doesn't contain the answer, say 'I don't have information
   about that.' Do NOT make up facts."

2. LOWER TEMPERATURE (0.0 - 0.3):
   Less randomness = more factual, less creative.

3. CHAIN-OF-THOUGHT WITH CITATIONS:
   "First quote the relevant passage from the context,
   then provide your answer based on that quote."
   Forces the model to ground its answer in source text.

4. RETRIEVAL QUALITY:
   Better retrieval = more relevant context = less hallucination.
   The model hallucinates when it doesn't have good context.

5. ANSWER VALIDATION:
   Run a second LLM call: "Does this answer match the context?
   Answer YES or NO."
   If NO, regenerate or flag for human review.

6. SOURCE ATTRIBUTION:
   Require the model to cite which document/chunk each claim
   comes from. Makes hallucination immediately visible.

7. CONSTRAINED GENERATION:
   Use structured output to limit what the model can say.
   Instead of free text, force it to select from options or
   fill in specific fields.

DETECTION:
  - Compare claims in the answer against the source chunks
  - Use NLI (Natural Language Inference) models
  - LLM-as-judge: "Rate the faithfulness of this answer 1-5"

INTERVIEW TIP: "I'd combine a strong system prompt, low temperature,
and chain-of-thought with citations. For critical applications, I'd
add a validation step that checks the answer against source context." """,
        "short": ["prompt", "temperature", "citation", "ground", "validate", "context"],
    },
    {
        "id": 30,
        "round": "Round 8: Practical Scenarios",
        "difficulty": "Hard",
        "type": "Scenario",
        "question": "Explain how you would build a customer support agent that can look up orders, check inventory, and process refunds.",
        "answer": """I'd build this as a TOOL-CALLING AGENT with LangGraph:

TOOLS (3 tools):
  @tool
  def lookup_order(order_id: str) -> str:
      \"\"\"Look up an order by ID. Returns order details.\"\"\"
      # Query database...

  @tool
  def check_inventory(product_id: str) -> str:
      \"\"\"Check if a product is in stock.\"\"\"
      # Query inventory system...

  @tool
  def process_refund(order_id: str, reason: str) -> str:
      \"\"\"Process a refund for an order. Requires order ID and reason.\"\"\"
      # Call payment API...

AGENT ARCHITECTURE:
  I'd use LangGraph (not a simple chain) because:
  1. The agent needs to DECIDE which tool to call
  2. Refunds need HUMAN APPROVAL (human-in-the-loop)
  3. Multi-step: might need to look up order, then check policy,
     then process refund

GRAPH:
  START -> agent_node -> tool_router
    -> lookup_order -> agent_node (loop back)
    -> check_inventory -> agent_node (loop back)
    -> process_refund -> human_approval -> agent_node
    -> no_tool_needed -> END

HUMAN-IN-THE-LOOP:
  For process_refund, add an interrupt() before execution.
  A human reviews: "Refund $49.99 for order #123 because
  'item arrived damaged'. Approve?"

SYSTEM PROMPT:
  "You are a customer support agent. You can look up orders,
  check inventory, and process refunds. Be polite and helpful.
  Always look up the order before processing a refund.
  For refunds over $100, explain that a manager needs to approve."

GUARDRAILS:
  - Validate order IDs before querying
  - Rate limit refund processing
  - Log all actions for audit

INTERVIEW TIP: "I'd use LangGraph with three tools, conditional
edges for routing, and human-in-the-loop for refunds. The system
prompt sets behavior guidelines and the graph handles the flow." """,
        "short": ["tool", "LangGraph", "human-in-the-loop", "interrupt", "system prompt", "route"],
    },
]


# =============================================================================
#  STUDY GUIDE MODE
# =============================================================================

def print_study_guide():
    """Print all questions with full answers for studying."""
    print()
    print("=" * 70)
    print("  LLM & AGENTS INTERVIEW STUDY GUIDE")
    print("  30 Questions with Detailed Answers")
    print("=" * 70)

    current_round = ""
    for q in QUESTIONS:
        if q["round"] != current_round:
            current_round = q["round"]
            print()
            print()
            print("=" * 70)
            print(f"  {current_round}")
            print("=" * 70)

        print()
        print(f"  Q{q['id']}. [{q['difficulty']}] [{q['type']}]")
        print(f"  {'-' * 60}")

        for line in q["question"].split("\n"):
            print(f"  {line}")

        if q.get("code"):
            print()
            print("  Code:")
            for line in q["code"].split("\n"):
                print(f"    {line}")

        print()
        print("  ANSWER:")
        for line in q["answer"].split("\n"):
            print(f"  {line}")

        print()
        print(f"  {'~' * 60}")

    print()
    print("=" * 70)
    print("  END OF STUDY GUIDE")
    print("=" * 70)
    print()
    print("  TIPS FOR YOUR LLM/AGENTS INTERVIEW:")
    print("  1. Know the RAG pipeline cold (load->split->embed->store->retrieve->generate)")
    print("  2. Be able to explain chains vs agents clearly")
    print("  3. Understand WHY you'd choose one approach over another")
    print("  4. Mention specific tools/libraries (LangChain, LangGraph, ChromaDB)")
    print("  5. For scenario questions, think out loud and be systematic")
    print("  6. It's OK to say 'I'd start simple with X, then iterate'")
    print()


# =============================================================================
#  INTERACTIVE QUIZ MODE
# =============================================================================

def run_quiz():
    """Run the interactive quiz in the terminal."""
    print()
    print("=" * 70)
    print("  LLM & AGENTS INTERVIEW QUIZ")
    print("  30 Questions | Type your answer, then see the full explanation")
    print("=" * 70)
    print()
    print("  HOW IT WORKS:")
    print("  - Each question shown one at a time")
    print("  - Type your answer (doesn't need to be perfect)")
    print("  - Press Enter to submit")
    print("  - You'll see the full answer + whether you hit key points")
    print("  - Type 'skip' to skip, 'quit' to exit early")
    print()
    input("  Press Enter to start... ")

    score = 0
    answered = 0
    skipped = 0
    results = []
    current_round = ""

    for q in QUESTIONS:
        if q["round"] != current_round:
            current_round = q["round"]
            print()
            print("=" * 70)
            print(f"  {current_round}")
            print("=" * 70)

        print()
        print(f"  Q{q['id']}/{len(QUESTIONS)} [{q['difficulty']}] [{q['type']}]")
        print(f"  {'-' * 60}")

        for line in q["question"].split("\n"):
            print(f"  {line}")

        if q.get("code"):
            print()
            print("  Code:")
            for line in q["code"].split("\n"):
                print(f"    {line}")

        print()

        try:
            user_answer = input("  Your answer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Quiz ended early.")
            break

        if user_answer.lower() == "quit":
            print("\n  Quiz ended early.")
            break

        if user_answer.lower() == "skip":
            skipped += 1
            results.append({"id": q["id"], "status": "skipped"})
            print("  Skipped!")
            print()
            print("  ANSWER:")
            for line in q["answer"].split("\n"):
                print(f"  {line}")
            input("\n  Press Enter for next question... ")
            continue

        answered += 1

        user_lower = user_answer.lower()
        hits = [kw for kw in q["short"] if kw.lower() in user_lower]
        hit_ratio = len(hits) / len(q["short"]) if q["short"] else 0

        if hit_ratio >= 0.4:
            score += 1
            status = "GOOD"
            verdict = "You hit the key points!"
        elif hit_ratio > 0:
            score += 0.5
            status = "PARTIAL"
            verdict = "You got some of it — read the full answer:"
        else:
            status = "MISS"
            verdict = "Review this one — here's the full answer:"

        results.append({
            "id": q["id"],
            "status": status,
            "hits": hits,
            "total_keywords": len(q["short"]),
        })

        print()
        print(f"  >> {verdict}")
        print()
        print("  FULL ANSWER:")
        for line in q["answer"].split("\n"):
            print(f"  {line}")

        try:
            input("\n  Press Enter for next question... ")
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Quiz ended early.")
            break

    # Score summary
    print()
    print("=" * 70)
    print("  QUIZ RESULTS")
    print("=" * 70)
    print()

    total_possible = answered
    percentage = (score / total_possible * 100) if total_possible > 0 else 0

    print(f"  Score: {score}/{total_possible} ({percentage:.0f}%)")
    print(f"  Answered: {answered}")
    print(f"  Skipped: {skipped}")
    print()

    if percentage >= 85:
        rating = "EXCELLENT"
        msg = "You're well-prepared for the LLM/agents portion!"
    elif percentage >= 70:
        rating = "GOOD"
        msg = "Solid foundation. Review the ones you missed."
    elif percentage >= 50:
        rating = "DECENT"
        msg = "You know the basics but study the LangChain/LangGraph chapters more."
    elif percentage >= 30:
        rating = "NEEDS WORK"
        msg = "Go through the langchain_course/ and langgraph_course/ chapters."
    else:
        rating = "KEEP STUDYING"
        msg = "Start with the course chapters, then retry this quiz!"

    print(f"  Rating: {rating}")
    print(f"  {msg}")
    print()

    missed = [r for r in results if r["status"] in ("MISS", "PARTIAL")]
    if missed:
        print("  REVIEW THESE QUESTIONS:")
        for r in missed:
            q_data = QUESTIONS[r["id"] - 1]
            marker = "~" if r["status"] == "PARTIAL" else "X"
            print(f"    [{marker}] Q{r['id']}: {q_data['question'].split(chr(10))[0][:55]}...")
        print()
        print("  Run with 'study' to see all answers:")
        print("    python interview_llms_and_agents.py study")

    print()
    print("=" * 70)
    print()


# =============================================================================
#  MAIN
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "study":
        print_study_guide()
    elif len(sys.argv) > 1 and sys.argv[1].lower() == "help":
        print()
        print("  Usage:")
        print("    python interview_llms_and_agents.py          Interactive quiz")
        print("    python interview_llms_and_agents.py study    Print study guide")
        print("    python interview_llms_and_agents.py help     Show this help")
        print()
    else:
        run_quiz()
