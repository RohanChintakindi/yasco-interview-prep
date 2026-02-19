"""
=====================================================
 CHAPTER 7: EMBEDDINGS
=====================================================

THIS IS THE KEY CONCEPT. If you understand embeddings, you understand RAG.

THE CORE IDEA
-------------
Computers can't understand words. They understand numbers.
Embeddings convert words/sentences/paragraphs into NUMBERS.

But not just any numbers - numbers that CAPTURE MEANING.

  "How do I cook pasta?"     -> [0.2, 0.8, 0.1, 0.5, ...]
  "What's the recipe for spaghetti?"  -> [0.21, 0.79, 0.12, 0.48, ...]
  "Explain quantum physics"  -> [0.9, 0.1, 0.7, 0.3, ...]

Notice: "cook pasta" and "recipe for spaghetti" have SIMILAR numbers!
They mean similar things, so their vectors are similar.

"Explain quantum physics" has VERY DIFFERENT numbers. Different meaning,
different vector.


HOW DO YOU MEASURE "SIMILAR"?
------------------------------
Cosine similarity. It measures the angle between two vectors.
  - 1.0 = identical meaning (vectors point the same direction)
  - 0.0 = completely unrelated (vectors are perpendicular)
  - Negative = opposite meaning (rare in practice)

You don't need to understand the math deeply. Just know:
  High cosine similarity = similar meaning
  Low cosine similarity = different meaning


WHY THIS MATTERS FOR RAG
-------------------------
Here's the magic:
  1. You embed all your document chunks and store the vectors
  2. When a user asks a question, you embed the question too
  3. You find which stored vectors are CLOSEST to the question vector
  4. Those closest chunks are the most relevant to the question
  5. You send those chunks to the LLM as context

This is SEMANTIC SEARCH - finding things by meaning, not by keywords.

Keyword search: "cook pasta" won't match "spaghetti recipe"
Semantic search: "cook pasta" WILL match "spaghetti recipe" (similar meaning!)


INSTALL:
  pip install langchain-huggingface sentence-transformers


HOW TO RUN THIS FILE:
  python ch7_embeddings.py

NOTE: This chapter uses HuggingFace embeddings. They're FREE, run
locally on your machine, and need NO API key. The first run will
download the model (~80MB) — after that it's cached and instant.
"""

from langchain_huggingface import HuggingFaceEmbeddings


# =============================================================================
# PART 1: CREATING AN EMBEDDING
# =============================================================================
#
# An embedding model takes text and returns a vector (list of numbers).
# The vector typically has 384 dimensions (for the all-MiniLM-L6-v2 model).
#
# "dimensions" = how many numbers in the list.
# 384 dimensions means each piece of text becomes a list of 384 numbers.
# These dimensions capture different aspects of meaning (topic, sentiment,
# formality, etc.) but they're not human-interpretable individually.

print("=" * 60)
print("PART 1: Creating an embedding")
print("=" * 60)

# Create the embedding model
# "all-MiniLM-L6-v2" is a great general-purpose model:
#   - 384 dimensions (compact but effective)
#   - Fast inference (runs on CPU just fine)
#   - Free, no API key needed
#   - First run downloads ~80MB, then it's cached locally
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Embed a single piece of text
vector = embeddings.embed_query("What is machine learning?")

print(f"Input: 'What is machine learning?'")
print(f"Output: a list of {len(vector)} numbers")
print(f"First 10 values: {vector[:10]}")
print(f"Each value is a float: {type(vector[0])}")
print()

# That's it. Text in, numbers out.
# These numbers encode the MEANING of "What is machine learning?"


# =============================================================================
# PART 2: embed_query() vs embed_documents()
# =============================================================================
#
# The embedding model has TWO methods:
#
#   embed_query("text")         -> for the QUESTION (single string -> single vector)
#   embed_documents(["texts"])  -> for your DATA (list of strings -> list of vectors)
#
# Why two methods? Some embedding models handle queries and documents
# slightly differently (they add prefixes like "search_query:" or
# "search_document:" internally). For best results, use the right one.
#
# Simple rule:
#   Embedding the user's question? -> embed_query()
#   Embedding your stored data?    -> embed_documents()

print("=" * 60)
print("PART 2: embed_query() vs embed_documents()")
print("=" * 60)

# For a single question:
query_vector = embeddings.embed_query("Who invented Python?")
print(f"Query vector: {len(query_vector)} dimensions")

# For multiple documents:
doc_vectors = embeddings.embed_documents([
    "Python was created by Guido van Rossum in 1991.",
    "JavaScript was created by Brendan Eich in 1995.",
    "The Earth orbits the Sun.",
])
print(f"Document vectors: {len(doc_vectors)} vectors, each {len(doc_vectors[0])} dimensions")
print()


# =============================================================================
# PART 3: MEASURING SIMILARITY
# =============================================================================
#
# Now the fun part: comparing vectors to find similar meanings.
#
# We'll use cosine similarity - the standard way to compare embeddings.
# It returns a number between -1 and 1:
#   ~1.0  = very similar meaning
#   ~0.5  = somewhat related
#   ~0.0  = unrelated
#   ~-1.0 = opposite meaning (rare)

print("=" * 60)
print("PART 3: Measuring similarity between texts")
print("=" * 60)


def cosine_similarity(vec_a, vec_b):
    """
    Calculate how similar two vectors are.
    Returns a number between -1 and 1.
    1.0 = identical direction (same meaning)
    0.0 = perpendicular (unrelated)
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a ** 2 for a in vec_a) ** 0.5
    magnitude_b = sum(b ** 2 for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


# Let's compare some sentences:
texts = {
    "cooking": "How do I cook pasta?",
    "recipe": "What's the recipe for spaghetti?",
    "quantum": "Explain quantum computing",
    "weather": "What's the weather like today?",
}

# Embed all of them
vectors = {name: embeddings.embed_query(text) for name, text in texts.items()}

# Compare each pair:
print("Similarity scores (higher = more similar meaning):\n")
pairs = [
    ("cooking", "recipe"),    # Should be HIGH (similar topic)
    ("cooking", "quantum"),   # Should be LOW (different topics)
    ("cooking", "weather"),   # Should be LOW
    ("quantum", "weather"),   # Should be LOW
]

for name_a, name_b in pairs:
    sim = cosine_similarity(vectors[name_a], vectors[name_b])
    print(f"  '{texts[name_a]}'")
    print(f"  vs '{texts[name_b]}'")
    print(f"  Similarity: {sim:.4f}")
    print()

# "cook pasta" vs "recipe for spaghetti" should be the highest!
# Different words, same meaning. That's the power of semantic search.


# =============================================================================
# PART 4: BUILD A MINI SEARCH ENGINE
# =============================================================================
#
# Let's build what a vector store does internally, from scratch.
# This is the heart of RAG retrieval.
#
#   1. We have a "database" of knowledge (5 sentences)
#   2. User asks a question
#   3. We find which sentences are most relevant
#
# In production, you'd use a vector store (Chapter 8) for this.
# But understanding the raw mechanics helps you debug and tune RAG.

print("=" * 60)
print("PART 4: Mini search engine (what vector stores do internally)")
print("=" * 60)

# Our "knowledge base"
knowledge = [
    "Python was created by Guido van Rossum in 1991.",
    "JavaScript was invented by Brendan Eich in just 10 days in 1995.",
    "The Earth orbits the Sun at approximately 67,000 miles per hour.",
    "Machine learning is a subset of artificial intelligence focused on learning from data.",
    "Water boils at 100 degrees Celsius at standard atmospheric pressure.",
    "LangChain is a framework for building applications powered by large language models.",
    "Neural networks are computing systems inspired by biological neural networks in the brain.",
]

# Step 1: Embed all our knowledge (this is the "indexing" phase)
print("Embedding knowledge base...")
knowledge_vectors = embeddings.embed_documents(knowledge)
print(f"Embedded {len(knowledge_vectors)} documents\n")

# Step 2: User asks a question
question = "Who made Python?"
print(f"Question: '{question}'")

# Step 3: Embed the question
question_vector = embeddings.embed_query(question)

# Step 4: Compare question to every document
print(f"\nRanked results:")
results = []
for i, doc_vector in enumerate(knowledge_vectors):
    similarity = cosine_similarity(question_vector, doc_vector)
    results.append((similarity, knowledge[i]))

# Sort by similarity (highest first)
results.sort(reverse=True)

for rank, (sim, text) in enumerate(results, 1):
    marker = " <-- TOP MATCH" if rank == 1 else ""
    print(f"  {rank}. [{sim:.4f}] {text}{marker}")

print()

# The top result should be about Guido van Rossum!
# That's semantic search: it found the answer even though our question
# says "made" not "created", and "Python" not "programming language".

# Step 5: In RAG, you'd take the top 2-3 results and send them
# to the LLM as context. That's what we build in Chapter 9.


# =============================================================================
# PART 5: TRY DIFFERENT QUESTIONS
# =============================================================================

print("=" * 60)
print("PART 5: More search examples")
print("=" * 60)

questions = [
    "Tell me about neural nets",
    "How hot does water need to be to bubble?",
    "What framework helps build AI apps?",
    "How fast does our planet move through space?",
]

for q in questions:
    q_vec = embeddings.embed_query(q)
    best_sim = -1
    best_doc = ""
    for doc_vec, doc_text in zip(knowledge_vectors, knowledge):
        sim = cosine_similarity(q_vec, doc_vec)
        if sim > best_sim:
            best_sim = sim
            best_doc = doc_text

    print(f"Q: '{q}'")
    print(f"A: [{best_sim:.4f}] {best_doc}")
    print()

# Notice how it matches:
# "neural nets" -> neural networks (different abbreviation, same meaning!)
# "bubble" -> boils (different word, same concept!)
# "AI apps" -> LangChain (understands the connection)
# "planet move through space" -> Earth orbits (rephrased completely)


# =============================================================================
# PART 6: EMBEDDING MODEL OPTIONS
# =============================================================================
#
# You have choices for embedding models:
#
#
# HUGGINGFACE (local, FREE) — what we're using in this chapter:
# -------------------------------------------------------------
#   pip install langchain-huggingface sentence-transformers
#
#   from langchain_huggingface import HuggingFaceEmbeddings
#   embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#
#   Pros: Completely free, works offline, no API key, data stays on your machine
#   Cons: Slightly lower quality than OpenAI, uses your CPU/GPU
#
#   Good model options:
#     "all-MiniLM-L6-v2"           # Fast, good quality (384 dims) <-- we use this
#     "all-mpnet-base-v2"          # Better quality, slower (768 dims)
#     "BAAI/bge-small-en-v1.5"     # Good balance (384 dims)
#
#
# OPENAI (cloud, paid) — if you need higher quality in production:
# ----------------------------------------------------------------
#   pip install langchain-openai
#
#   from langchain_openai import OpenAIEmbeddings
#   embeddings = OpenAIEmbeddings(model="text-embedding-3-small")   # 1536 dims
#   embeddings = OpenAIEmbeddings(model="text-embedding-3-large")   # 3072 dims
#
#   Pros: Higher quality, easy to use
#   Cons: Costs money (~$0.02 per 1M tokens), requires API key, data leaves your machine
#
#
# WHICH SHOULD YOU USE?
#   Learning/prototyping: HuggingFace (free!)       <-- that's us right now
#   Production with budget: OpenAI text-embedding-3-small
#   Production, highest quality: OpenAI text-embedding-3-large
#   Privacy-sensitive: HuggingFace (data never leaves your machine)
#
#
# IMPORTANT: Once you embed your documents with a model, you MUST use the
# same model to embed queries. You can't embed docs with OpenAI and search
# with HuggingFace — the vectors would be in completely different spaces.


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Setup (HuggingFace — free, local):
#   embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#
# Setup (OpenAI — paid, cloud):
#   embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
#
# Embed a question:
#   vector = embeddings.embed_query("my question")  -> list of floats
#
# Embed documents:
#   vectors = embeddings.embed_documents(["doc1", "doc2"])  -> list of vectors
#
# Key concepts:
#   - Embeddings capture MEANING as numbers
#   - Similar meaning = similar vectors = high cosine similarity
#   - This enables semantic search (find by meaning, not keywords)
#   - Use same model for documents AND queries
#
# =============================================================================
