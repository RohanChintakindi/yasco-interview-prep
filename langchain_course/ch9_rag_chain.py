"""
=====================================================
 CHAPTER 9: RAG (RETRIEVAL-AUGMENTED GENERATION)
=====================================================

THIS IS THE CHAPTER. Everything we've learned comes together here.

WHAT IS RAG?
------------
RAG stands for Retrieval-Augmented Generation. Let's break that down:

  Retrieval:  Find relevant information from your data
  Augmented:  Add that information to the prompt
  Generation: Let the LLM generate an answer using that context

WHY DO WE NEED RAG?
--------------------
LLMs have two big problems:

  1. KNOWLEDGE CUTOFF: They only know what they were trained on.
     GPT-4 doesn't know about events after its training date.
     It doesn't know about YOUR company's internal docs, YOUR codebase,
     or YOUR personal notes.

  2. HALLUCINATION: When LLMs don't know something, they make stuff up.
     Confidently. With a straight face. They'll invent fake citations,
     fake statistics, fake API endpoints.

RAG solves both:
  - You provide YOUR data as context, so the LLM doesn't need to "know" it
  - You tell the LLM to answer ONLY from the context, reducing hallucination


THE RAG FLOW (WHAT HAPPENS WHEN A USER ASKS A QUESTION):
---------------------------------------------------------

  User: "What is LCEL?"
        |
        v
  [Retriever] -> Searches vector store -> Finds 3 relevant chunks:
        |          "LCEL uses the pipe operator..."
        |          "Chains are sequences of calls..."
        |          "Everything is a Runnable..."
        v
  [Prompt Template] -> Builds this message:
        |   SYSTEM: "Answer based on this context:
        |            LCEL uses the pipe operator...
        |            Chains are sequences of calls...
        |            Everything is a Runnable..."
        |   HUMAN: "What is LCEL?"
        v
  [LLM] -> Generates answer using ONLY the provided context
        |
        v
  "LCEL (LangChain Expression Language) uses the pipe operator (|)
   to connect Runnables into chains..."

The LLM never searches Google. It never makes stuff up. It reads the
context you provided and answers based on that. That's RAG.


INSTALL:
  pip install langchain-openai langchain-chroma langchain-text-splitters chromadb


HOW TO RUN THIS FILE:
  python ch9_rag_chain.py
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0.2,
)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# =============================================================================
# STEP 1: BUILD THE KNOWLEDGE BASE
# =============================================================================
#
# In a real app, this data would come from:
#   - Document loaders (Ch5): PDFs, web pages, text files
#   - Then split with text splitters (Ch6)
#   - Then embedded and stored (Ch7-8)
#
# Here we'll use sample text and go through the full pipeline in one file.

print("=" * 60)
print("STEP 1: Building the knowledge base")
print("=" * 60)

# Pretend this is a document you loaded from somewhere
raw_text = """
# LangChain Framework Documentation

## Overview
LangChain is a framework for developing applications powered by large language models.
It was created by Harrison Chase and first released in October 2022.
The framework provides tools for prompt management, chains, data augmented generation,
agents, memory, and evaluation.

## Core Concepts

### Chains
Chains are sequences of calls to LLMs or other utilities. The simplest chain takes
a prompt, sends it to an LLM, and returns the response. More complex chains combine
multiple steps. LangChain Expression Language (LCEL) uses the pipe operator (|) to
connect components into chains. Each component is a Runnable.

### Prompts
Prompt templates help create structured inputs for LLMs. ChatPromptTemplate supports
system, human, and AI messages. Templates can include variables using {curly_braces}
syntax that get filled in at runtime.

### Document Loaders
Document loaders bring data from various sources into LangChain's Document format.
Supported sources include text files, PDFs, web pages, CSVs, databases, and APIs.
Each document has page_content (text) and metadata (source info).

### Text Splitters
Text splitters break documents into smaller chunks for processing.
RecursiveCharacterTextSplitter is the recommended default splitter. It splits on
natural boundaries: paragraphs, then lines, then words. Typical chunk sizes range
from 200 to 1000 characters with 10-20% overlap between chunks.

### Embeddings
Embeddings convert text into numerical vectors that capture semantic meaning.
Similar texts produce similar vectors, enabling semantic search.
OpenAI's text-embedding-3-small is a popular choice. Embeddings enable finding
documents by meaning rather than just keyword matching.

### Vector Stores
Vector stores are databases optimized for similarity search over embeddings.
ChromaDB, FAISS, Pinecone, and Weaviate are popular options. ChromaDB is free
and runs locally, making it ideal for development and small projects.

### RAG (Retrieval-Augmented Generation)
RAG combines retrieval with generation. Instead of relying solely on the LLM's
training data, RAG retrieves relevant documents and includes them in the prompt.
This grounds the LLM's response in actual data, reducing hallucination and
enabling the LLM to answer questions about your specific data.

## Installation
Install LangChain with: pip install langchain langchain-openai langchain-community
For vector stores: pip install langchain-chroma chromadb
For text splitting: pip install langchain-text-splitters

## Key Principles
1. Everything is a Runnable with .invoke(), .stream(), .batch()
2. LCEL pipe syntax (|) connects Runnables into chains
3. Documents are the universal data format (page_content + metadata)
4. Retrieval is the key to grounding LLM responses in facts
""".strip()


# STEP 1a: Split into chunks
# Why chunk_size=400? Because our sample text is short. For real data,
# you'd use 500-1000. See Chapter 6 for guidance.
splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
chunks = splitter.split_text(raw_text)

# Convert to Documents with metadata
documents = [
    Document(
        page_content=chunk,
        metadata={"source": "langchain_docs", "chunk_index": i}
    )
    for i, chunk in enumerate(chunks)
]

print(f"Original text: {len(raw_text)} characters")
print(f"Split into: {len(documents)} chunks")
print()

# STEP 1b: Create vector store (embeds all chunks automatically)
vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
print(f"Stored {vectorstore._collection.count()} chunks in vector store")
print()


# =============================================================================
# STEP 2: CREATE THE RETRIEVER
# =============================================================================
#
# The retriever is the "search" component. Given a question, it finds
# the most relevant chunks from the vector store.
#
# Remember from Ch8: .as_retriever() converts a vector store into a
# Runnable. This means it plugs directly into LCEL chains.

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Quick test: what does the retriever return?
print("=" * 60)
print("STEP 2: Testing the retriever")
print("=" * 60)

test_docs = retriever.invoke("What is LCEL?")
print(f"Query: 'What is LCEL?'")
print(f"Retrieved {len(test_docs)} chunks:\n")
for i, doc in enumerate(test_docs, 1):
    print(f"  Chunk {i}: {doc.page_content[:80]}...")
print()


# =============================================================================
# STEP 3: THE RAG PROMPT
# =============================================================================
#
# This is the prompt that brings context and question together.
#
# The SYSTEM message is crucial. It tells the LLM:
#   1. Here's the context (the retrieved chunks)
#   2. Answer ONLY from this context
#   3. If the context doesn't have the answer, say so
#
# That third point is important: it prevents hallucination.
# Without it, the LLM might answer from its training data instead
# of your provided context.

rag_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant. Answer the user's question based ONLY "
     "on the following context. If the context doesn't contain enough "
     "information to answer, say 'I don't have enough information to answer "
     "that based on the provided context.'\n\n"
     "Context:\n{context}"),
    ("human", "{question}"),
])

# The prompt needs two variables:
#   {context}  - the retrieved chunks (as a string)
#   {question} - the user's question


# =============================================================================
# STEP 4: THE format_docs HELPER
# =============================================================================
#
# The retriever returns a LIST of Document objects.
# But the prompt template needs a STRING for {context}.
#
# format_docs converts: [Document, Document, Document] -> "text\n---\ntext\n---\ntext"
#
# This is a simple but essential glue function.

def format_docs(docs):
    """Convert a list of Documents into a single string for the prompt."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

# Example:
# [Doc("hello"), Doc("world")] -> "hello\n\n---\n\nworld"


# =============================================================================
# STEP 5: BUILD THE RAG CHAIN
# =============================================================================
#
# HERE IT IS. The core RAG chain. Let's build it step by step.
#
# Remember from Chapter 4: a dict in LCEL is a RunnableParallel.
# It runs multiple operations at the same time and collects results
# into a dict.

print("=" * 60)
print("STEP 5: The RAG chain")
print("=" * 60)

rag_chain = (
    # STEP A: Prepare the inputs (runs in PARALLEL)
    {
        "context": retriever | format_docs,
        #          ^^^^^^^^   ^^^^^^^^^^^
        #          |          |
        #          |          Convert [Doc, Doc, Doc] -> "text\n---\ntext"
        #          |
        #          Takes the question string, returns [Doc, Doc, Doc]

        "question": RunnablePassthrough(),
        #           ^^^^^^^^^^^^^^^^^^^^
        #           Takes the question string, passes it through unchanged
    }
    # After this step, we have: {"context": "chunk texts...", "question": "user question"}

    | rag_prompt        # STEP B: Fill the template -> messages
    | llm               # STEP C: Send to LLM -> AIMessage
    | StrOutputParser()  # STEP D: Extract text -> string
)

# LET'S TRACE THROUGH A REAL CALL:
#
# rag_chain.invoke("What is LCEL?")
#
# Step A (parallel):
#   "context" path:
#     "What is LCEL?" -> retriever -> [Doc("LCEL uses pipe..."), Doc("Chains are..."), Doc("Everything is...")]
#     [Doc, Doc, Doc] -> format_docs -> "LCEL uses pipe...\n---\nChains are...\n---\nEverything is..."
#
#   "question" path:
#     "What is LCEL?" -> RunnablePassthrough -> "What is LCEL?"
#
#   Result: {"context": "LCEL uses pipe...\n---\n...", "question": "What is LCEL?"}
#
# Step B:
#   rag_prompt fills in {context} and {question} -> [SystemMessage(...), HumanMessage(...)]
#
# Step C:
#   llm receives messages -> AIMessage("LCEL stands for LangChain Expression Language...")
#
# Step D:
#   StrOutputParser -> "LCEL stands for LangChain Expression Language..."


# =============================================================================
# STEP 6: ASK QUESTIONS!
# =============================================================================

print()
print("=" * 60)
print("STEP 6: RAG in action!")
print("=" * 60)

questions = [
    "What is LangChain and who created it?",
    "How do text splitters work?",
    "What is LCEL and how does it work?",
    "What vector stores can I use?",
    "What is the meaning of life?",  # NOT in our data!
]

for question in questions:
    print(f"\nQ: {question}")
    answer = rag_chain.invoke(question)
    print(f"A: {answer}")

print()

# Notice the last question: "What is the meaning of life?"
# The context doesn't contain this information, so the LLM should say
# "I don't have enough information" (because we told it to in the prompt).
# This is EXACTLY what we want - no hallucination!


# =============================================================================
# STEP 7: RAG WITH SOURCES (CITATIONS)
# =============================================================================
#
# In a real app, you often want to show users WHERE the answer came from.
# "According to langchain_docs, chunk 3..."
#
# The trick: retrieve the documents separately so you can access them
# for both the chain AND for displaying sources.

print("=" * 60)
print("STEP 7: RAG with source citations")
print("=" * 60)

def ask_with_sources(question: str):
    """Ask a question and return both the answer and source documents."""
    # Step 1: Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)

    # Step 2: Build the context string
    context = format_docs(retrieved_docs)

    # Step 3: Build a simple chain (no retriever needed - we already have context)
    answer_chain = rag_prompt | llm | StrOutputParser()

    # Step 4: Get the answer
    answer = answer_chain.invoke({
        "context": context,
        "question": question,
    })

    return answer, retrieved_docs


question = "What are embeddings used for?"
answer, sources = ask_with_sources(question)

print(f"Q: {question}")
print(f"A: {answer}")
print(f"\nSources used:")
for i, doc in enumerate(sources, 1):
    chunk_idx = doc.metadata['chunk_index']
    preview = doc.page_content[:80].replace('\n', ' ')
    print(f"  {i}. [Chunk {chunk_idx}] {preview}...")
print()


# =============================================================================
# STEP 8: RAG WITH STREAMING
# =============================================================================
#
# For a chatbot UX, you want the answer to stream in word by word.
# Since our chain is made of Runnables, .stream() works automatically!

print("=" * 60)
print("STEP 8: Streaming RAG")
print("=" * 60)

question = "How does RAG reduce hallucination?"
print(f"Q: {question}")
print("A: ", end="")

for chunk in rag_chain.stream(question):
    print(chunk, end="", flush=True)

print("\n")


# =============================================================================
# THE COMPLETE RAG PIPELINE - VISUAL SUMMARY
# =============================================================================
#
# INDEXING PHASE (done once, before any questions):
#
#   [Raw Data: files, web pages, PDFs]
#        |
#   [Document Loader]          (Ch5)
#        |  Loads raw data into Document objects
#        v
#   [Text Splitter]            (Ch6)
#        |  Breaks documents into small chunks
#        v
#   [Embedding Model]          (Ch7)
#        |  Converts each chunk into a vector
#        v
#   [Vector Store]             (Ch8)
#        |  Stores vectors for fast search
#        v
#   [Done! Data is indexed and ready]
#
#
# QUERY PHASE (every time a user asks a question):
#
#   [User Question: "What is LCEL?"]
#        |
#        |----> [Retriever]                (Ch8)
#        |         |  Searches vector store
#        |         |  Returns top k chunks
#        |         v
#        |      [format_docs]
#        |         |  Joins chunks into a string
#        |         v
#        |      {context: "chunk texts..."}
#        |
#        |----> {question: "What is LCEL?"}  (RunnablePassthrough)
#        |
#        v
#   [RAG Prompt Template]                  (Ch2)
#        |  "Context: {context}\n\nQuestion: {question}"
#        v
#   [LLM]                                  (Ch1)
#        |  Generates answer from context
#        v
#   [StrOutputParser]                      (Ch3)
#        |  Extracts text
#        v
#   [Answer: "LCEL is LangChain Expression Language..."]
#
#
# EVERY chapter built up to this moment:
#   Ch1: How to call an LLM
#   Ch2: How to structure prompts with messages
#   Ch3: How to parse LLM output
#   Ch4: How to chain components with LCEL
#   Ch5: How to load data from files/web
#   Ch6: How to split data into chunks
#   Ch7: How embeddings capture meaning
#   Ch8: How vector stores enable fast search
#   Ch9: How RAG puts it ALL together
#
# Next: Chapter 10 - A real project that scrapes the web and builds
# a full RAG chatbot you can actually use!
