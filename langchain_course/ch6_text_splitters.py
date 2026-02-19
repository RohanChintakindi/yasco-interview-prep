"""
=====================================================
 CHAPTER 6: TEXT SPLITTERS
=====================================================

THE PROBLEM
-----------
In Chapter 5, we loaded documents. But there's a problem:

A Wikipedia page might be 50,000 characters long.
A PDF textbook might be 500 pages.

You can't just shove all of that into an LLM prompt. Two reasons:
  1. LLMs have a CONTEXT WINDOW limit (e.g., 128k tokens).
     Even if your doc fits, sending too much text is expensive and slow.
  2. More importantly: PRECISION. If someone asks "What is photosynthesis?"
     and you send a 500-page biology textbook, the LLM has to find the
     needle in the haystack. It might miss it or get confused.

THE SOLUTION: split documents into small, focused CHUNKS.

Instead of searching one 50,000 character document, you search
500 chunks of ~100 characters each. When someone asks about
photosynthesis, you find the 3-4 most relevant chunks and send
ONLY those to the LLM. Cheaper, faster, more accurate.

But HOW you split matters a lot. Bad splitting = bad RAG.


WHY SPLITTING STRATEGY MATTERS
-------------------------------
Imagine this paragraph:

  "Python was created by Guido van Rossum. He started working on
   it in the late 1980s and released version 1.0 in 1994."

If you split at 40 characters:
  Chunk 1: "Python was created by Guido van Rossu"   <- name cut off!
  Chunk 2: "m. He started working on it in the lat"  <- meaningless fragment
  Chunk 3: "e 1980s and released version 1.0 in 19"  <- year cut off!

This is terrible. Each chunk is meaningless on its own.

If you split on sentence boundaries:
  Chunk 1: "Python was created by Guido van Rossum."
  Chunk 2: "He started working on it in the late 1980s and released version 1.0 in 1994."

Much better! Each chunk is a complete thought.

That's what RecursiveCharacterTextSplitter does - it tries to split
at the most natural boundary possible.


INSTALL:
  pip install langchain-text-splitters


HOW TO RUN THIS FILE:
  python ch6_text_splitters.py
"""

from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_core.documents import Document


# =============================================================================
# PART 1: CharacterTextSplitter - THE SIMPLE (BUT DUMB) WAY
# =============================================================================
#
# CharacterTextSplitter splits on a SINGLE separator. You tell it:
#   "Split on newlines" or "Split on periods" or "Split on spaces"
#
# It then combines pieces until it reaches chunk_size, and creates a chunk.
#
# It's simple and predictable, but can only split on ONE boundary type.

print("=" * 60)
print("PART 1: CharacterTextSplitter")
print("=" * 60)

text = """Python is a programming language. It was created by Guido van Rossum.
Python is known for its simple syntax. It is used in web development and AI.
Python has a large community. There are thousands of packages available.
Python supports multiple paradigms including OOP and functional programming."""

splitter = CharacterTextSplitter(
    separator="\n",       # Split on newlines
    chunk_size=100,       # Target max size per chunk (in characters)
    chunk_overlap=20,     # Overlap between adjacent chunks
)

chunks = splitter.split_text(text)

print(f"Original: {len(text)} characters")
print(f"Chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"\n  Chunk {i} ({len(chunk)} chars): '{chunk}'")
print()

# WHAT IS chunk_overlap?
# ----------------------
# When you split text into chunks, information at the BOUNDARIES gets lost.
# If a sentence spans two chunks, it gets cut.
#
# Overlap means the end of chunk N is repeated at the start of chunk N+1.
#
# Without overlap:
#   Chunk 1: "...about photosynthesis."
#   Chunk 2: "This process converts..."
#   (If searching for "photosynthesis process", neither chunk has both words)
#
# With 20 char overlap:
#   Chunk 1: "...about photosynthesis."
#   Chunk 2: "photosynthesis. This process converts..."
#   (Now chunk 2 has both words - it can be found by search!)
#
# Rule of thumb: overlap = 10-20% of chunk_size.


# =============================================================================
# PART 2: RecursiveCharacterTextSplitter - THE ONE YOU SHOULD USE
# =============================================================================
#
# THIS IS THE DEFAULT. Use this unless you have a specific reason not to.
#
# Instead of splitting on ONE separator, it tries MULTIPLE separators
# in order of preference:
#
#   1. "\n\n" (paragraph breaks) - BEST boundary
#   2. "\n"   (line breaks)
#   3. " "    (spaces between words)
#   4. ""     (individual characters) - LAST RESORT
#
# It tries to split at the most meaningful boundary first.
# Only falls back to less meaningful boundaries for chunks that are still
# too big after the higher-level split.
#
# "Recursive" means: split on paragraphs first. If a paragraph is still
# too long, recursively split it on lines. If a line is still too long,
# split on words. Etc.

print("=" * 60)
print("PART 2: RecursiveCharacterTextSplitter (THE DEFAULT)")
print("=" * 60)

long_text = """
# Introduction to Machine Learning

Machine learning is a branch of artificial intelligence that focuses on building
systems that learn from data. Instead of explicitly programming rules, ML algorithms
find patterns in data and make decisions with minimal human intervention.

## Types of Machine Learning

There are three main types of machine learning:

### Supervised Learning

In supervised learning, the algorithm learns from labeled training data. Each training
example has an input and a known correct output. The algorithm learns to map inputs to
outputs. Common examples include image classification, spam detection, and price prediction.

Supervised learning is the most common type in practice. You need a labeled dataset,
which means someone has already tagged each example with the correct answer.

### Unsupervised Learning

Unsupervised learning works with unlabeled data. The algorithm tries to find hidden
patterns or structures without being told what to look for. Clustering (grouping similar
items) and dimensionality reduction are common unsupervised techniques.

### Reinforcement Learning

In reinforcement learning, an agent learns by interacting with an environment. It
receives rewards or penalties for its actions and learns to maximize cumulative reward.
This approach powers game-playing AI, robotics, and autonomous vehicles.

## Why Machine Learning Matters

ML is everywhere: recommendation systems (Netflix, Spotify), voice assistants (Siri),
self-driving cars, medical diagnosis, fraud detection, and much more. Understanding
ML is becoming essential for software engineers and data scientists.
""".strip()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,     # Each chunk should be roughly 300 characters
    chunk_overlap=50,   # 50 characters of overlap
)

chunks = splitter.split_text(long_text)

print(f"Original: {len(long_text)} characters")
print(f"Chunks: {len(chunks)}")
print()
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i} ({len(chunk)} chars) ---")
    print(chunk)
    print()

# Notice how it splits on paragraph boundaries (double newlines) first,
# keeping related sentences together. Much more meaningful than splitting
# every N characters blindly.


# =============================================================================
# PART 3: SPLITTING DOCUMENTS (NOT JUST STRINGS)
# =============================================================================
#
# In practice, you'll split Document objects (from loaders), not raw strings.
# Use .split_documents() instead of .split_text().
#
# The crucial thing: METADATA IS PRESERVED. When you split a Document
# into 10 chunks, all 10 chunks get the same metadata (source, page, etc.)
# So you always know where each chunk came from.

print("=" * 60)
print("PART 3: Splitting Documents (metadata preserved)")
print("=" * 60)

doc = Document(
    page_content=long_text,
    metadata={"source": "ml_textbook.pdf", "chapter": 1, "author": "Dr. Smith"},
)

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
split_docs = splitter.split_documents([doc])

print(f"1 document -> {len(split_docs)} chunks")
print()

# Check that metadata is preserved:
for i, d in enumerate(split_docs[:3]):
    print(f"Chunk {i}:")
    print(f"  Source: {d.metadata['source']}")
    print(f"  Chapter: {d.metadata['chapter']}")
    print(f"  Preview: {d.page_content[:60]}...")
    print()

# Every chunk knows it came from "ml_textbook.pdf", chapter 1, by Dr. Smith.
# When RAG retrieves chunk 7, you can tell the user:
# "According to ml_textbook.pdf (chapter 1)..."


# =============================================================================
# PART 4: CHOOSING chunk_size AND chunk_overlap
# =============================================================================
#
# This is more art than science. Here are guidelines:
#
# chunk_size (in characters):
# ---------------------------
#   50-100:   Way too small. Chunks are fragments, lose context.
#             "Guido van" is useless without "Rossum" and "created Python".
#
#   200-500:  Good for most use cases. Each chunk is roughly a paragraph.
#             Contains a complete thought. Good balance of precision and context.
#             ** START HERE: chunk_size=500 **
#
#   500-1000: Bigger chunks = more context per chunk, but less precise search.
#             Good when your data has long, interconnected explanations.
#
#   1000+:    Usually too big. Defeats the purpose of splitting.
#             Search becomes imprecise again.
#
# chunk_overlap:
# --------------
#   0:          No overlap. Risk losing info at boundaries.
#   10-20% of chunk_size: GOOD DEFAULT. chunk_size=500 -> overlap=50-100.
#   50%+:       Too much. Redundant storage, wasted embedding compute.
#
# MY RECOMMENDATION:
#   Start with chunk_size=500, chunk_overlap=50.
#   Test your RAG pipeline with real questions.
#   If answers are too vague: decrease chunk_size (more precise chunks).
#   If answers lack context: increase chunk_size (more context per chunk).

print("=" * 60)
print("PART 4: Comparing different chunk sizes")
print("=" * 60)

for size in [100, 300, 500, 1000]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=50)
    chunks = splitter.split_text(long_text)
    print(f"chunk_size={size:>4} -> {len(chunks):>2} chunks, avg {sum(len(c) for c in chunks)//len(chunks)} chars each")
print()


# =============================================================================
# PART 5: SPECIALIZED SPLITTERS
# =============================================================================
#
# RecursiveCharacterTextSplitter is the default, but specialized splitters
# exist for specific content types:
#
#
# FOR CODE:
# ---------
#   from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
#
#   python_splitter = RecursiveCharacterTextSplitter.from_language(
#       language=Language.PYTHON,
#       chunk_size=500,
#       chunk_overlap=50,
#   )
#   # This splits on function/class boundaries instead of paragraphs.
#   # So a Python function stays in one chunk rather than getting split mid-function.
#   # Supports: PYTHON, JAVASCRIPT, TYPESCRIPT, GO, RUST, JAVA, and more.
#
#
# FOR MARKDOWN:
# -------------
#   from langchain_text_splitters import MarkdownHeaderTextSplitter
#
#   splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
#       ("#", "Header 1"),
#       ("##", "Header 2"),
#   ])
#   # Splits on markdown headers and adds the header text to metadata.
#   # So a chunk from under "## Machine Learning > ### Supervised Learning"
#   # will have metadata: {"Header 1": "Machine Learning", "Header 2": "Supervised Learning"}
#
#
# FOR HTML:
# ---------
#   from langchain_text_splitters import HTMLHeaderTextSplitter
#   # Same idea as Markdown splitter, but for HTML tags (<h1>, <h2>, etc.)


# =============================================================================
# SUMMARY: WHERE TEXT SPLITTING FITS IN RAG
# =============================================================================
#
#   [Documents from Loader]    <- Ch5: "entire Wikipedia page" (50,000 chars)
#           |
#   [Text Splitter]            <- THIS CHAPTER: split into ~100 chunks of ~500 chars
#           |
#   [Embeddings]               <- Ch7: convert each chunk to a vector
#           |
#   [Vector Store]             <- Ch8: store all vectors for fast search
#           |
#   [Retriever]                <- Ch8: "find the 3 chunks most relevant to my question"
#           |
#   [RAG Chain]                <- Ch9: send those 3 chunks + question to LLM
#
# Text splitting is the bridge between "raw data" and "searchable chunks".


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Default splitter (USE THIS):
#   splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#
# Split raw text:
#   chunks = splitter.split_text("long text here...")  -> list of strings
#
# Split Documents (preserves metadata):
#   split_docs = splitter.split_documents([doc1, doc2])  -> list of Documents
#
# For code:
#   splitter = RecursiveCharacterTextSplitter.from_language(Language.PYTHON, ...)
#
# =============================================================================
