"""
=====================================================
 CHAPTER 10: FINAL PROJECT - WEB SCRAPING RAG PIPELINE
=====================================================

THE CAPSTONE
------------
This is the final project. We're building a REAL application that:

  1. SCRAPES web pages (you pick the URLs)
  2. SPLITS the content into searchable chunks
  3. EMBEDS and stores them in a vector database
  4. Lets you CHAT with the scraped content
  5. STREAMS responses in real time
  6. Maintains CONVERSATION HISTORY across turns

This is a legit app. Companies charge money for products that do
exactly this. You're building it from scratch.

HOW IT WORKS:
  You give it URLs (Wikipedia pages, documentation, articles, etc.)
  It scrapes them, processes them, and creates a chatbot that can
  answer questions about the content of those pages.

  You: "Who created Python?"
  Bot: "According to the scraped Wikipedia page, Python was created
       by Guido van Rossum and first released in 1991."

  The bot isn't making this up - it's reading from the actual
  scraped content. That's RAG in action.


ARCHITECTURE:
  ┌─────────────────────────────────────────────────┐
  │                                                 │
  │  URLs ──> WebBaseLoader ──> Raw Documents       │
  │                                │                │
  │               RecursiveCharacterTextSplitter    │
  │                                │                │
  │                          Chunks (Documents)     │
  │                                │                │
  │  OpenAI Embeddings ──> Vectors │                │
  │                                │                │
  │                         ChromaDB (Vector Store) │
  │                                │                │
  │  User Question ──> Retriever ──┤                │
  │                                │                │
  │                    RAG Prompt + LLM             │
  │                                │                │
  │                    Streamed Answer              │
  │                                                 │
  └─────────────────────────────────────────────────┘


INSTALL:
  pip install langchain-openai langchain-chroma langchain-community
  pip install langchain-text-splitters chromadb beautifulsoup4 python-dotenv


HOW TO RUN:
  python ch10_project_web_scraping_rag.py
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import shutil

load_dotenv()


# =============================================================================
# CONFIGURATION
# =============================================================================
# Change these to customize the app!

# LLM settings (using Grok via x.ai)
LLM_MODEL = "grok-4-1-fast-non-reasoning"
LLM_BASE_URL = "https://api.x.ai/v1"
LLM_TEMPERATURE = 0.2

# Embedding model
EMBEDDING_MODEL = "text-embedding-3-small"

# Vector store location (saved to disk so you don't re-embed on restart)
CHROMA_DIR = "./project_chroma_db"

# Text splitting settings (see Ch6 for guidance)
CHUNK_SIZE = 500       # Characters per chunk
CHUNK_OVERLAP = 50     # Overlap between chunks

# How many chunks to retrieve per question
RETRIEVAL_K = 4

# URLs TO SCRAPE - Change these to whatever you want to learn about!
# The bot will be able to answer questions about these pages.
URLS = [
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Large_language_model",
]


# =============================================================================
# STEP 1: SCRAPE
# =============================================================================
# Uses WebBaseLoader from Chapter 5.
# Each URL becomes one Document with the page's text content.

def scrape_urls(urls: list[str]):
    """
    Scrape text content from a list of URLs.

    WebBaseLoader uses BeautifulSoup to:
      1. Fetch the HTML from each URL
      2. Strip tags, scripts, styles
      3. Extract just the text content
      4. Return as Documents with metadata (source URL, title, etc.)
    """
    print(f"  Scraping {len(urls)} URLs...")
    loader = WebBaseLoader(urls)
    docs = loader.load()

    for doc in docs:
        title = doc.metadata.get("title", doc.metadata.get("source", "unknown"))
        print(f"    Loaded: {title}")
        print(f"      Characters: {len(doc.page_content):,}")

    return docs


# =============================================================================
# STEP 2: CHUNK
# =============================================================================
# Uses RecursiveCharacterTextSplitter from Chapter 6.
# Breaks each document into smaller, searchable pieces.

def chunk_documents(docs):
    """
    Split documents into smaller chunks.

    Why? Because if we search the entire Wikipedia page as one unit,
    we always get the entire page. By splitting into chunks, we can
    find the specific PARAGRAPH that answers the question.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(docs)
    print(f"\n  Split {len(docs)} pages into {len(chunks)} chunks")
    print(f"  Average chunk size: {sum(len(c.page_content) for c in chunks) // len(chunks)} chars")
    return chunks


# =============================================================================
# STEP 3: EMBED & STORE
# =============================================================================
# Uses OpenAIEmbeddings (Ch7) and ChromaDB (Ch8).
# Each chunk gets converted to a vector and stored for fast search.

def create_vector_store(chunks):
    """
    Embed all chunks and store in ChromaDB.

    This is the most expensive step (API calls for embedding).
    That's why we persist to disk - so we only do this once.
    """
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    # Clean previous store (start fresh each run)
    shutil.rmtree(CHROMA_DIR, ignore_errors=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )

    count = vectorstore._collection.count()
    print(f"\n  Embedded and stored {count} chunks in {CHROMA_DIR}")
    return vectorstore


# =============================================================================
# STEP 4: BUILD THE RAG CHAIN
# =============================================================================
# Combines retriever + prompt + LLM from Chapter 9.
# Added: conversation history support (MessagesPlaceholder from Ch2).

def build_rag_chain(vectorstore):
    """
    Build the RAG chain with conversation history.

    This chain:
      1. Takes a question + chat history
      2. Retrieves relevant chunks from the vector store
      3. Formats them into a prompt with the system instructions
      4. Sends to the LLM
      5. Returns the text response
    """
    llm = ChatOpenAI(
        model=LLM_MODEL,
        base_url=LLM_BASE_URL,
        temperature=LLM_TEMPERATURE,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVAL_K})

    # The RAG prompt with conversation history
    # This is the same pattern from Ch2 (MessagesPlaceholder) + Ch9 (RAG prompt)
    rag_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful research assistant. You answer questions based on "
         "content scraped from web pages.\n\n"
         "RULES:\n"
         "1. Answer based on the provided context below.\n"
         "2. If the context doesn't contain enough info, say so honestly.\n"
         "3. Be specific and cite details from the context.\n"
         "4. Keep answers concise but thorough.\n\n"
         "Context from scraped web pages:\n{context}"),
        # Chat history goes here (0 to N previous messages)
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])

    def format_docs(docs):
        """Format retrieved documents with their source URL."""
        formatted = []
        for doc in docs:
            source = doc.metadata.get("source", "unknown")
            formatted.append(f"[Source: {source}]\n{doc.page_content}")
        return "\n\n---\n\n".join(formatted)

    # The RAG chain
    # Note: we use lambdas here instead of RunnablePassthrough because
    # our input is a dict with multiple keys (question, chat_history)
    rag_chain = (
        {
            "context": lambda x: format_docs(retriever.invoke(x["question"])),
            "question": lambda x: x["question"],
            "chat_history": lambda x: x.get("chat_history", []),
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# =============================================================================
# STEP 5: INTERACTIVE CHAT
# =============================================================================
# A chat loop with:
#   - Streaming responses (word by word, like ChatGPT)
#   - Conversation history (the bot remembers what you talked about)
#   - Commands: "quit" to exit, "clear" to reset history

def chat(rag_chain):
    """
    Interactive chat loop.

    Maintains conversation history so the bot can reference previous
    messages. For example:
      You: "What year was Python created?"
      Bot: "Python was first released in 1991."
      You: "Who created it?"         <- "it" refers to Python from above
      Bot: "Guido van Rossum."       <- Bot understands from context

    The history is sent with every request (LLMs are stateless, remember Ch2).
    We trim to the last 10 exchanges to avoid hitting token limits.
    """
    print("\n" + "=" * 60)
    print("  RAG CHATBOT")
    print("  Ask questions about the scraped web pages!")
    print("  Commands: 'quit' to exit, 'clear' to reset history")
    print("=" * 60)

    chat_history = []

    while True:
        # Get user input
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() == "quit":
            print("Goodbye!")
            break
        if question.lower() == "clear":
            chat_history = []
            print("(Chat history cleared)")
            continue

        # Stream the response (word by word)
        print("Bot: ", end="", flush=True)
        full_response = ""

        for chunk in rag_chain.stream({
            "question": question,
            "chat_history": chat_history,
        }):
            print(chunk, end="", flush=True)
            full_response += chunk

        print()  # Newline after streaming

        # Add this exchange to history (Ch2: multi-turn conversations)
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=full_response))

        # Trim history to last 10 exchanges (20 messages) to manage token usage
        # Each exchange = 1 HumanMessage + 1 AIMessage = 2 messages
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]


# =============================================================================
# MAIN - RUN THE FULL PIPELINE
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  WEB SCRAPING RAG PIPELINE")
    print("  Chapters 1-9 combined into one application")
    print("=" * 60)
    print()

    # --- INDEXING PHASE (done once) ---
    print("[1/3] SCRAPING WEB PAGES")
    docs = scrape_urls(URLS)

    print("\n[2/3] CHUNKING DOCUMENTS")
    chunks = chunk_documents(docs)

    print("\n[3/3] EMBEDDING & STORING")
    vectorstore = create_vector_store(chunks)

    # --- QUERY PHASE (interactive) ---
    rag_chain = build_rag_chain(vectorstore)
    chat(rag_chain)

    # --- CLEANUP ---
    # Comment out the next line if you want to keep the vector store
    # (so you can reload it without re-scraping and re-embedding)
    shutil.rmtree(CHROMA_DIR, ignore_errors=True)
    print("\nCleaned up vector store.")


# =============================================================================
# WHAT YOU'VE LEARNED - THE COMPLETE LANGCHAIN JOURNEY
# =============================================================================
#
# Ch1:  LLM Basics
#       ChatOpenAI, .invoke(), .stream(), .batch()
#       Everything is a Runnable.
#
# Ch2:  Messages & Prompts
#       SystemMessage, HumanMessage, AIMessage
#       ChatPromptTemplate, MessagesPlaceholder
#       LLMs are stateless - you send full history every time.
#
# Ch3:  Output Parsers
#       StrOutputParser, JsonOutputParser
#       .with_structured_output() for typed Pydantic objects
#
# Ch4:  Chains & LCEL
#       The | pipe operator, RunnableLambda, RunnablePassthrough
#       RunnableParallel (dicts), chain composition, .bind()
#
# Ch5:  Document Loaders
#       TextLoader, WebBaseLoader, CSVLoader, PyPDFLoader
#       Documents = page_content + metadata
#
# Ch6:  Text Splitters
#       RecursiveCharacterTextSplitter (the default)
#       chunk_size, chunk_overlap, splitting strategy
#
# Ch7:  Embeddings
#       Text -> vectors, cosine similarity, semantic search
#       embed_query() vs embed_documents()
#
# Ch8:  Vector Stores
#       ChromaDB, similarity_search(), .as_retriever()
#       Persistence, metadata filtering
#
# Ch9:  RAG Chains
#       Retriever + format_docs + prompt + LLM = grounded answers
#       Sources/citations, streaming RAG
#
# Ch10: This project
#       All of the above, combined into a real application.
#
#
# WHERE TO GO NEXT:
# -----------------
# 1. Try different URLs - documentation sites, news articles, blog posts
# 2. Add PDF support - swap WebBaseLoader for PyPDFLoader
# 3. Build a web UI - add Streamlit or Gradio for a visual interface
# 4. Try local embeddings - HuggingFace for free, offline embedding
# 5. Explore Agents - LLMs that can use TOOLS (search, calculate, code)
# 6. LangSmith - debugging and monitoring tool for LangChain apps
# 7. LangGraph - for building complex, multi-step AI workflows
#
# =============================================================================
