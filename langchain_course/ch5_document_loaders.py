"""
=====================================================
 CHAPTER 5: DOCUMENT LOADERS
=====================================================

WHERE WE ARE IN THE RAG JOURNEY
---------------------------------
Chapters 1-4 taught you how to talk to LLMs and build chains.
Now we start the DATA side. RAG needs data, and that data comes
from somewhere: files, websites, PDFs, databases, etc.

Document Loaders are the FIRST step in the RAG pipeline:

  [YOUR DATA] -> Document Loader -> Documents -> ... -> RAG

Their job is simple: take data from any source and convert it into
LangChain's universal format: the Document object.


WHAT IS A DOCUMENT?
-------------------
A Document is just two things:

  Document(
      page_content = "the actual text...",      # The content
      metadata = {"source": "file.pdf", ...}    # Where it came from
  )

That's it. Every loader in LangChain - whether it loads a .txt file,
a web page, a PDF, a CSV, or a YouTube transcript - produces Documents.

Why metadata? Because in RAG, when the AI gives an answer, you want to
know WHERE that answer came from. "According to page 42 of report.pdf..."
Metadata makes this possible.


INSTALL:
  pip install langchain-community beautifulsoup4


HOW TO RUN THIS FILE:
  python ch5_document_loaders.py
"""

from langchain_community.document_loaders import (
    TextLoader,
    WebBaseLoader,
    CSVLoader,
)
from langchain_core.documents import Document


# =============================================================================
# PART 1: CREATING DOCUMENTS BY HAND
# =============================================================================
#
# Before using loaders, let's understand what they produce.
# You can create Documents manually - they're just Python objects.

print("=" * 60)
print("PART 1: What is a Document?")
print("=" * 60)

doc = Document(
    page_content="LangChain is a framework for building LLM applications.",
    metadata={"source": "my_notes.txt", "author": "me", "page": 1},
)

print(f"Content: {doc.page_content}")
print(f"Metadata: {doc.metadata}")
print(f"Source: {doc.metadata['source']}")
print()

# That's all a Document is. Loaders just automate creating these.


# =============================================================================
# PART 2: TextLoader - LOADING .TXT FILES
# =============================================================================
#
# The simplest loader. Reads an entire text file into ONE Document.
#
# TextLoader("file.txt").load() -> [Document(page_content="entire file...")]
#
# The metadata will include {"source": "file.txt"}.

print("=" * 60)
print("PART 2: TextLoader - Loading text files")
print("=" * 60)

# First, let's create a sample file to work with
sample_text = """Artificial Intelligence (AI) is the simulation of human intelligence by machines.

Machine Learning (ML) is a subset of AI where systems learn from data without
being explicitly programmed. Instead of writing rules, you give the system
examples and it figures out the patterns.

Deep Learning is a subset of ML that uses neural networks with many layers.
These "deep" networks can learn very complex patterns, which is why they're
so good at things like image recognition and language understanding.

Large Language Models (LLMs) are deep learning models trained on massive
amounts of text data. They learn to predict the next word in a sequence,
and through this simple task, they develop a broad understanding of language,
facts, and reasoning. GPT, Claude, and LLaMA are examples of LLMs.
"""

with open("sample_data.txt", "w") as f:
    f.write(sample_text)

# Now load it:
loader = TextLoader("sample_data.txt")
docs = loader.load()

print(f"Number of documents: {len(docs)}")  # 1 - the whole file is one doc
print(f"Content length: {len(docs[0].page_content)} characters")
print(f"Metadata: {docs[0].metadata}")
print(f"Preview: {docs[0].page_content[:100]}...")
print()

# KEY POINT: TextLoader puts the ENTIRE file into ONE Document.
# Later (Chapter 6), we'll split this into smaller chunks.


# =============================================================================
# PART 3: WebBaseLoader - SCRAPING WEB PAGES
# =============================================================================
#
# This loader fetches a web page, strips the HTML, and gives you the text.
# Under the hood, it uses BeautifulSoup (a popular HTML parsing library).
#
# This is how you build a "chat with any website" app:
#   1. Scrape the site with WebBaseLoader
#   2. Split into chunks (Ch6)
#   3. Embed and store (Ch7-8)
#   4. RAG chain (Ch9)
#
# One Document per URL. Metadata includes title, source URL, language, etc.

print("=" * 60)
print("PART 3: WebBaseLoader - Scraping web pages")
print("=" * 60)

# Load a single page:
loader = WebBaseLoader("https://en.wikipedia.org/wiki/Python_(programming_language)")
docs = loader.load()

print(f"Number of documents: {len(docs)}")
print(f"Content length: {len(docs[0].page_content)} characters")
print(f"Metadata: {list(docs[0].metadata.keys())}")
print(f"Title: {docs[0].metadata.get('title', 'N/A')}")
print(f"Preview: {docs[0].page_content[:200]}...")
print()

# Load MULTIPLE pages at once:
print("Loading multiple URLs...")
loader = WebBaseLoader([
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://en.wikipedia.org/wiki/JavaScript",
])
docs = loader.load()
print(f"Loaded {len(docs)} documents from 2 URLs")
print()

# IMPORTANT: Web scraping gives you MESSY text. The page content will include
# navigation menus, footers, sidebar text, etc. It's not perfectly clean.
# For production apps, you'd want to:
#   - Use more specific selectors (BeautifulSoup kwargs)
#   - Clean the text before processing
#   - Or use a dedicated web scraping service


# =============================================================================
# PART 4: CSVLoader - STRUCTURED DATA
# =============================================================================
#
# CSVLoader is different from the others: each ROW becomes its own Document.
# This makes sense because each row is a separate "thing" (a person, a
# product, a record, etc.)
#
# The page_content contains the row data as key-value pairs.
# The metadata includes the source file and row number.

print("=" * 60)
print("PART 4: CSVLoader - One document per row")
print("=" * 60)

# Create a sample CSV
import csv

with open("sample_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["language", "year_created", "creator", "paradigm"])
    writer.writerow(["Python", "1991", "Guido van Rossum", "Multi-paradigm"])
    writer.writerow(["JavaScript", "1995", "Brendan Eich", "Multi-paradigm"])
    writer.writerow(["Rust", "2010", "Graydon Hoare", "Systems"])
    writer.writerow(["Go", "2009", "Robert Griesemer, Rob Pike, Ken Thompson", "Compiled"])

loader = CSVLoader("sample_data.csv")
docs = loader.load()

print(f"Number of documents: {len(docs)}")  # 4 - one per data row
print()
for i, doc in enumerate(docs):
    print(f"Document {i}:")
    print(f"  Content: {doc.page_content}")
    print(f"  Metadata: {doc.metadata}")
    print()

# Notice how each row became a Document with the data in key: value format.
# The CSV headers became the keys.


# =============================================================================
# PART 5: LAZY LOADING - FOR BIG DATASETS
# =============================================================================
#
# .load() reads EVERYTHING into memory at once. Fine for small files,
# but if you have 10GB of documents, your computer runs out of RAM.
#
# .lazy_load() returns a GENERATOR - it loads one document at a time.
# You process one, and it loads the next. Memory efficient.
#
# Think of it like:
#   .load()      = open the entire book and photocopy every page
#   .lazy_load() = open the book and read one page at a time

print("=" * 60)
print("PART 5: Lazy Loading")
print("=" * 60)

loader = TextLoader("sample_data.txt")

# Eager (loads all at once):
docs = loader.load()
print(f"Eager: loaded {len(docs)} docs (all in memory)")

# Lazy (loads one at a time):
count = 0
for doc in loader.lazy_load():
    count += 1
    print(f"Lazy: processing doc {count} ({len(doc.page_content)} chars)")
print()

# For TextLoader with one file, there's no real difference.
# But for DirectoryLoader with 1000 files, lazy_load prevents memory issues.


# =============================================================================
# PART 6: OTHER LOADERS YOU SHOULD KNOW ABOUT
# =============================================================================
#
# LangChain has 100+ document loaders. Here are the most useful ones:
#
#
# PDF FILES (very common for RAG):
# --------------------------------
#   pip install pypdf
#   from langchain_community.document_loaders import PyPDFLoader
#   loader = PyPDFLoader("document.pdf")
#   docs = loader.load()  # One Document PER PAGE (page number in metadata)
#
#   This is probably the most popular loader after WebBaseLoader.
#   Each page becomes its own Document, so metadata["page"] tells you
#   which page the info came from. Great for citing sources.
#
#
# DIRECTORY OF FILES (load everything in a folder):
# --------------------------------------------------
#   from langchain_community.document_loaders import DirectoryLoader
#   loader = DirectoryLoader("./my_docs/", glob="**/*.txt")
#   docs = loader.load()  # Loads ALL matching files
#
#   glob="**/*.txt"  -> all .txt files in all subdirectories
#   glob="**/*.pdf"  -> all PDFs
#   glob="**/*.md"   -> all Markdown files
#
#
# YOUTUBE TRANSCRIPTS:
# --------------------
#   pip install youtube-transcript-api
#   from langchain_community.document_loaders import YoutubeLoader
#   loader = YoutubeLoader.from_youtube_url("https://youtube.com/watch?v=...")
#   docs = loader.load()
#
#   Loads the transcript of a YouTube video. Great for building a
#   "chat with YouTube videos" app.
#
#
# JSON:
# -----
#   from langchain_community.document_loaders import JSONLoader
#   loader = JSONLoader("data.json", jq_schema=".messages[].content")
#   # jq_schema tells it where to find the text in the JSON structure
#
#
# THE PATTERN:
#   1. Find the right loader for your data source
#   2. loader = SomeLoader("path or URL")
#   3. docs = loader.load()
#   4. Each doc has .page_content and .metadata
#   5. Feed docs into text splitter (Chapter 6)


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Text files:
#   TextLoader("file.txt").load()          -> [1 doc with full file]
#
# Web pages:
#   WebBaseLoader("https://...").load()    -> [1 doc per URL]
#   WebBaseLoader(["url1", "url2"]).load() -> [1 doc per URL]
#
# CSV:
#   CSVLoader("file.csv").load()           -> [1 doc per row]
#
# PDF:
#   PyPDFLoader("file.pdf").load()         -> [1 doc per page]
#
# Directory:
#   DirectoryLoader("./dir/", glob="**/*.txt").load() -> [1 doc per file]
#
# All loaders produce: Document(page_content=str, metadata=dict)
#
# =============================================================================

# CLEANUP
import os
os.remove("sample_data.txt")
os.remove("sample_data.csv")
