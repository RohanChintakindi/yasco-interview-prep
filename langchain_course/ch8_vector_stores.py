"""
=====================================================
 CHAPTER 8: VECTOR STORES
=====================================================

IN CHAPTER 7, WE DID THIS MANUALLY:
  1. Embedded all documents
  2. Stored vectors in a Python list
  3. Looped through every vector to find the closest match

That works for 7 documents. But what about 100,000? Or 10 million?
Looping through millions of vectors for every search query would be
painfully slow.

VECTOR STORES solve this. They're specialized databases designed for
one thing: finding the most similar vectors FAST.

Under the hood, they use clever algorithms (like HNSW, IVF, etc.)
that don't need to compare against every single vector. They use
approximate nearest neighbor search to find close matches in
milliseconds, even with millions of vectors.

Think of it like a library:
  - Chapter 7: You have a stack of books and flip through each one
  - Chapter 8: You have a library with a card catalog system


WE'LL USE ChromaDB:
  - Free, open source
  - Runs locally (no cloud account needed)
  - No setup (just pip install)
  - Perfect for learning and small-to-medium projects
  - In production, you might use Pinecone, Weaviate, or FAISS instead


INSTALL:
  pip install langchain-chroma chromadb


HOW TO RUN THIS FILE:
  python ch8_vector_stores.py
"""

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# =============================================================================
# PART 1: CREATING A VECTOR STORE
# =============================================================================
#
# The vector store handles embedding AND storage in one step.
# You give it Documents, it:
#   1. Extracts the page_content from each Document
#   2. Sends it to the embedding model
#   3. Gets back vectors
#   4. Stores the vectors alongside the original text and metadata
#
# Later, when you search, it:
#   1. Embeds your search query
#   2. Finds the closest stored vectors
#   3. Returns the original Documents for those vectors

print("=" * 60)
print("PART 1: Creating a vector store from Documents")
print("=" * 60)

# Imagine these came from a document loader + text splitter.
# In reality you'd have hundreds or thousands of chunks.
documents = [
    Document(
        page_content="Python was created by Guido van Rossum and first released in 1991.",
        metadata={"source": "python_wiki", "topic": "history"},
    ),
    Document(
        page_content="JavaScript was created by Brendan Eich in 1995 while working at Netscape.",
        metadata={"source": "js_wiki", "topic": "history"},
    ),
    Document(
        page_content="Rust is a systems programming language focused on safety, speed, and concurrency.",
        metadata={"source": "rust_wiki", "topic": "overview"},
    ),
    Document(
        page_content="Machine learning is a subset of AI that enables systems to learn from data.",
        metadata={"source": "ml_textbook", "topic": "definition"},
    ),
    Document(
        page_content="PyPI (Python Package Index) hosts over 500,000 third-party Python packages.",
        metadata={"source": "python_wiki", "topic": "ecosystem"},
    ),
    Document(
        page_content="React is a JavaScript library for building user interfaces, developed by Meta.",
        metadata={"source": "react_docs", "topic": "overview"},
    ),
    Document(
        page_content="Neural networks are computing systems inspired by biological neural networks in the brain.",
        metadata={"source": "ml_textbook", "topic": "concepts"},
    ),
    Document(
        page_content="Python supports multiple paradigms: procedural, object-oriented, and functional programming.",
        metadata={"source": "python_wiki", "topic": "features"},
    ),
]

# Create the vector store - this embeds all documents automatically
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    # collection_name="my_collection",  # optional: name for this collection
)

print(f"Created vector store with {vectorstore._collection.count()} documents")
print("(All documents were embedded and stored automatically)")
print()

# What just happened:
#   1. Chroma took each Document's page_content
#   2. Sent all 8 texts to the embedding model (API calls)
#   3. Got back 8 vectors (each 1536 dimensions)
#   4. Stored each vector + original text + metadata in its internal database


# =============================================================================
# PART 2: SIMILARITY SEARCH
# =============================================================================
#
# This is the core operation. You ask a question, it returns the most
# relevant documents.
#
# Behind the scenes:
#   1. Your question is embedded (converted to a vector)
#   2. The vector store finds the k closest vectors to your question's vector
#   3. It returns the original Documents for those vectors

print("=" * 60)
print("PART 2: Similarity search")
print("=" * 60)

# k=3 means "return the 3 most relevant documents"
results = vectorstore.similarity_search("Who created Python?", k=3)

print("Query: 'Who created Python?'\n")
print(f"Top {len(results)} results:")
for i, doc in enumerate(results, 1):
    print(f"\n  {i}. [{doc.metadata['source']}] {doc.page_content}")

print()

# The top result should be about Guido van Rossum.
# Even though we asked "Who created" and the doc says "was created by",
# the embedding model understands they mean the same thing.

# Let's try another:
results = vectorstore.similarity_search("Tell me about neural networks", k=2)
print("Query: 'Tell me about neural networks'\n")
for i, doc in enumerate(results, 1):
    print(f"  {i}. [{doc.metadata['source']}] {doc.page_content}")
print()


# =============================================================================
# PART 3: SIMILARITY SEARCH WITH SCORES
# =============================================================================
#
# Sometimes you want to know HOW similar the results are.
# Was the top result a great match (0.95) or a mediocre one (0.4)?
#
# similarity_search_with_score() returns (Document, score) tuples.
#
# IMPORTANT: Chroma returns DISTANCE, not similarity.
#   Distance 0.0 = perfect match (identical)
#   Distance 1.0 = somewhat related
#   Distance 2.0 = very different
#   LOWER is BETTER (opposite of cosine similarity!)

print("=" * 60)
print("PART 3: Search with scores (lower distance = better match)")
print("=" * 60)

results = vectorstore.similarity_search_with_score("What is machine learning?", k=4)

print("Query: 'What is machine learning?'\n")
for doc, score in results:
    quality = "GREAT" if score < 0.5 else "OK" if score < 1.0 else "WEAK"
    print(f"  [{quality}] Distance: {score:.4f} | {doc.page_content[:60]}...")
print()

# You can use scores to filter out bad matches:
#   if score > 1.5:
#       print("No good matches found")
# This prevents the LLM from getting irrelevant context.


# =============================================================================
# PART 4: METADATA FILTERING
# =============================================================================
#
# What if you only want to search within specific documents?
#
# Example: You have docs from multiple sources, but you only want
# results from "python_wiki". Metadata filtering does this.
#
# This is like SQL WHERE clauses, but for vector search:
#   "Find the most similar documents WHERE source = 'python_wiki'"

print("=" * 60)
print("PART 4: Metadata filtering")
print("=" * 60)

# Search ONLY in python_wiki documents:
results = vectorstore.similarity_search(
    "programming features",
    k=3,
    filter={"source": "python_wiki"},
)

print("Query: 'programming features' (filtered to source='python_wiki')\n")
for i, doc in enumerate(results, 1):
    print(f"  {i}. [{doc.metadata['source']}] {doc.page_content[:70]}...")
print()

# Without filtering, results might include Rust and JS docs.
# With filtering, only Python docs are returned.

# You can filter on ANY metadata key:
results = vectorstore.similarity_search(
    "what is this about?",
    k=2,
    filter={"topic": "history"},  # Only "history" topic docs
)
print("Filtered to topic='history':")
for doc in results:
    print(f"  [{doc.metadata['topic']}] {doc.page_content[:60]}...")
print()


# =============================================================================
# PART 5: .as_retriever() - THE BRIDGE TO RAG CHAINS
# =============================================================================
#
# This is the CRUCIAL step that connects vector stores to LCEL chains.
#
# A Retriever is a Runnable that:
#   Input:  a string (the search query)
#   Output: a list of Documents (the search results)
#
# Because it's a Runnable, it plugs directly into chains with |:
#
#   retriever | format_docs | prompt | llm | parser
#
# .as_retriever() converts a vector store into a Retriever.

print("=" * 60)
print("PART 5: .as_retriever() - Converting to a Runnable")
print("=" * 60)

retriever = vectorstore.as_retriever(
    search_type="similarity",   # Default. Other option: "mmr" (more diverse results)
    search_kwargs={"k": 3},     # Return top 3 results
)

# The retriever is a Runnable - use .invoke() just like anything else
docs = retriever.invoke("What web framework uses JavaScript?")

print("Query: 'What web framework uses JavaScript?'\n")
for doc in docs:
    print(f"  [{doc.metadata['source']}] {doc.page_content[:60]}...")
print()

# This retriever is what we'll plug into the RAG chain in Chapter 9!
# It's the piece that says "given a question, find relevant context."
#
# SEARCH TYPES:
#   "similarity" - Returns the k most similar documents.
#     Simple, fast, usually good enough.
#
#   "mmr" (Maximum Marginal Relevance) - Returns DIVERSE results.
#     If the top 3 results all say the same thing, MMR will instead
#     return 1 highly relevant + 2 related-but-different docs.
#     Better for getting a rounded answer. Slightly slower.


# =============================================================================
# PART 6: PERSISTING TO DISK
# =============================================================================
#
# By default, Chroma stores everything in memory. When your script ends,
# the data disappears. Every time you restart, you'd have to re-embed
# all documents (which costs API calls = money and time).
#
# persist_directory saves the database to disk. Next time, you can
# load it instantly without re-embedding.

print("=" * 60)
print("PART 6: Saving to disk and loading back")
print("=" * 60)

# Save to disk:
persistent_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db",  # Creates this folder
)
print(f"Saved {persistent_store._collection.count()} docs to ./chroma_db")

# Later (even in a different script), load it back:
loaded_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,  # Need same embedding model!
)
print(f"Loaded {loaded_store._collection.count()} docs from disk")

# Search works just like before:
results = loaded_store.similarity_search("Python history", k=1)
print(f"Search result: {results[0].page_content[:60]}...")
print()

# IMPORTANT: You MUST use the same embedding model when loading!
# If you saved with OpenAI embeddings, you must load with OpenAI embeddings.
# The vectors are meaningless with a different model.

# Cleanup
import shutil
shutil.rmtree("./chroma_db", ignore_errors=True)
print("Cleaned up ./chroma_db")
print()


# =============================================================================
# PART 7: ADDING DOCUMENTS AFTER CREATION
# =============================================================================
#
# You don't have to create a vector store all at once.
# You can add more documents later.

print("=" * 60)
print("PART 7: Adding documents incrementally")
print("=" * 60)

# Start with a few docs:
store = Chroma.from_documents(
    documents=documents[:3],
    embedding=embeddings,
)
print(f"Started with {store._collection.count()} docs")

# Add more later:
store.add_documents(documents[3:])
print(f"After adding more: {store._collection.count()} docs")
print()

# This is useful for:
# - Adding new data over time (new articles, new documents)
# - Processing large datasets in batches
# - Building a growing knowledge base


# =============================================================================
# PART 8: OTHER VECTOR STORES
# =============================================================================
#
# ChromaDB is great for learning. Here's the landscape:
#
# LOCAL (runs on your machine):
# -----------------------------
#   ChromaDB - What we're using. Easy, free, good for dev.
#
#   FAISS (Facebook AI Similarity Search):
#     pip install faiss-cpu langchain-community
#     from langchain_community.vectorstores import FAISS
#     # Very fast. Good for medium datasets (100k-1M docs).
#     # Used by Meta internally. No server needed.
#
#
# CLOUD (managed service):
# ------------------------
#   Pinecone:
#     pip install langchain-pinecone
#     # Managed cloud service. Scales to billions of vectors.
#     # Free tier available. Best for production.
#
#   Weaviate, Qdrant, Milvus:
#     # Other cloud/self-hosted options with different tradeoffs.
#
#
# WHEN TO USE WHAT:
#   Learning/prototyping:  ChromaDB (simplest)
#   Small production:      ChromaDB or FAISS
#   Large production:      Pinecone or Weaviate
#   Need speed, no cloud:  FAISS
#   Need managed service:  Pinecone
#
#
# THE GREAT NEWS: LangChain abstracts the differences!
# All vector stores have .similarity_search() and .as_retriever().
# You can swap ChromaDB for Pinecone by changing ~3 lines of code.


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Create from documents:
#   store = Chroma.from_documents(documents, embeddings)
#   store = Chroma.from_documents(documents, embeddings, persist_directory="./db")
#
# Search:
#   docs = store.similarity_search("query", k=3)
#   docs_with_scores = store.similarity_search_with_score("query", k=3)
#
# Filter:
#   docs = store.similarity_search("query", k=3, filter={"key": "value"})
#
# Convert to Retriever (for LCEL chains):
#   retriever = store.as_retriever(search_kwargs={"k": 3})
#   docs = retriever.invoke("query")
#
# Add more documents:
#   store.add_documents([new_doc1, new_doc2])
#
# Load from disk:
#   store = Chroma(persist_directory="./db", embedding_function=embeddings)
#
# =============================================================================
