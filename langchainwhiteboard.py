# from langchain_community.document_loaders import TextLoader, CSVLoader, WebBaseLoader, PyPDFLoader
# from langchain_core.documents import Document

# doc = Document(
#     page_content = "Langchain is a framework for building LLM applications.",
#     metadata = {"source": "my_notes.txt", "author" : "me", "page" : 1}
# )

# print(doc.page_content)
# print(doc.metadata)
# print(doc.metadata["source"])

# sample_text = """Artificial Intelligence (AI) is the simulation of human intelligence by machines.

# Machine Learning (ML) is a subset of AI where systems learn from data without
# being explicitly programmed. Instead of writing rules, you give the system
# examples and it figures out the patterns.

# Deep Learning is a subset of ML that uses neural networks with many layers.
# These "deep" networks can learn very complex patterns, which is why they're
# so good at things like image recognition and language understanding.

# Large Language Models (LLMs) are deep learning models trained on massive
# amounts of text data. They learn to predict the next word in a sequence,
# and through this simple task, they develop a broad understanding of language,
# facts, and reasoning. GPT, Claude, and LLaMA are examples of LLMs.
# """

# with open("sample_data1.txt", "w") as f:
#     f.write(sample_text)


# loader = TextLoader("sample_data.txt")
# docs = loader.load()

# print(len(docs))
# print(len(docs[0].page_content))
# print(docs[0].metadata)
# print(docs[0].page_content[:100])

# loader = WebBaseLoader("https://en.wikipedia.org/wiki/Python_(programming_language)")
# docs = loader.load()

# print(len(docs))
# print(len(docs[0].page_content))
# print(docs[0].metadata)
# print(docs[0].metadata.get('title', 'N/A'))
# print(docs[0].page_content[:200])


# loader = WebBaseLoader([
#     "https://en.wikipedia.org/wiki/Python_(programming_language)",
#     "https://en.wikipedia.org/wiki/JavaScript",
# ])

# docs = loader.load()

# print(len(docs))

# import csv

# with open("sample_data.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["language", "year_created", "creator", "paradigm"])
#     writer.writerow(["Python", "1991", "Guido van Rossum", "Multi-paradigm"])
#     writer.writerow(["JavaScript", "1995", "Brendan Eich", "Multi-paradigm"])
#     writer.writerow(["Rust", "2010", "Graydon Hoare", "Systems"])
#     writer.writerow(["Go", "2009", "Robert Griesemer, Rob Pike, Ken Thompson", "Compiled"])

# loader = CSVLoader("sample_data.csv")
# docs = loader.load()

# print(len(docs))
# for i, doc in enumerate(docs):
#     print(i)
#     print(doc.page_content)
#     print(doc.metadata)

# loader = TextLoader("sample_data.txt")
# docs = loader.lazy_load()


# # loader = PyPDFLoader("document.pdf")
# # docs = loader.load()

# from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter, Language

# text = """Python is a programming language. It was created by Guido van Rossum.
# Python is known for its simple syntax. It is used in web development and AI.
# Python has a large community. There are thousands of packages available.
# Python supports multiple paradigms including OOP and functional programming."""

# splitter = CharacterTextSplitter(
#     separator = "\n",
#     chunk_size = 100,
#     chunk_overlap = 20
# )

# chunks = splitter.split_text(text)

# print(len(text))
# print(len(chunks))

# for i, chunk in enumerate(chunks):
#     print(f"\n  Chunk {i} ({len(chunk)} chars): '{chunk}'")

# # 10 - 20% of chunk size

# long_text = """
# # Introduction to Machine Learning

# Machine learning is a branch of artificial intelligence that focuses on building
# systems that learn from data. Instead of explicitly programming rules, ML algorithms
# find patterns in data and make decisions with minimal human intervention.

# ## Types of Machine Learning

# There are three main types of machine learning:

# ### Supervised Learning

# In supervised learning, the algorithm learns from labeled training data. Each training
# example has an input and a known correct output. The algorithm learns to map inputs to
# outputs. Common examples include image classification, spam detection, and price prediction.

# Supervised learning is the most common type in practice. You need a labeled dataset,
# which means someone has already tagged each example with the correct answer.

# ### Unsupervised Learning

# Unsupervised learning works with unlabeled data. The algorithm tries to find hidden
# patterns or structures without being told what to look for. Clustering (grouping similar
# items) and dimensionality reduction are common unsupervised techniques.

# ### Reinforcement Learning

# In reinforcement learning, an agent learns by interacting with an environment. It
# receives rewards or penalties for its actions and learns to maximize cumulative reward.
# This approach powers game-playing AI, robotics, and autonomous vehicles.

# ## Why Machine Learning Matters

# ML is everywhere: recommendation systems (Netflix, Spotify), voice assistants (Siri),
# self-driving cars, medical diagnosis, fraud detection, and much more. Understanding
# ML is becoming essential for software engineers and data scientists.
# """.strip()

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 300,
#     chunk_overlap = 50
# )

# chunks = splitter.split_text(long_text)

# for i, chunk in enumerate(chunks):
#     print(f"--- Chunk {i} ({len(chunk)} chars) ---")
#     print(chunk)
#     print()


# doc = Document(
#     page_content = long_text,
#     metadata = {"source": "ml_textbook.pdf", "chapter" : 1, "author" : "Dr. Smith"}
# )

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 300,
#     chunk_overlap = 50
# )

# split_docs = splitter.split_documents([doc])
# print(len(split_docs))
# print(type(split_docs))
# for i, doc in enumerate(split_docs):
#     print(i, doc.page_content)
#     print(doc.metadata)
#     print(type(doc))

# # 500 is a good chunk size
# # 10 - 20% chunk_size


# python_splitter = RecursiveCharacterTextSplitter.from_language(
#     language = Language.PYTHON,
#     chunk_size = 500,
#     chunk_overlap = 50
# )

# # cosine similarity
# # higher = similar meaning

# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatOpenAI(
#     model="grok-4-1-fast-non-reasoning",
#     base_url="https://api.x.ai/v1",
#     temperature=0.2
# )

# response = llm.invoke("What is Python in one sentence")
# print(response.content)
# print(response.response_metadata)
# print(response.id)
# print(type(response))
# print(response.content.upper())

# # AIMessage Object

# chunks = llm.stream("What is Python in 3 sentences?")

# #AIMessageChunks

# for chunk in chunks:
#     print(chunk.content, end = "", flush=True)

# questions = ["What is 3 + 1 and explain why?",
#                              "What is 4 + 1 and explain why?",
#                              "What is 5 + 1 and explain why?"]

# batch_response  = llm.batch(questions)

# for question, response in zip(questions, batch_response):
#     print(f"Q: {question}")
#     print(f"A: {response.content}")
#     print()

# from langchain_huggingface import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
# vector = embeddings.embed_query("What is maching learning?")

# print(vector)
# print(len(vector))
# print(type(vector[0]))

# query_vector = embeddings.embed_query("Who invented Python?")
# print(len(query_vector))

# doc_vectors = embeddings.embed_documents([
#     "Python was created by Guido van Rossum in 1991.",
#     "JavaScript was created by Brendan Eich in 1995.",
#     "The Earth orbits the Sun."
# ])

# print(len(doc_vectors))
# print(len(doc_vectors[0]))


# def cosine_similarity(vec_a, vec_b):
#     dot_product = sum( a * b for a,b in zip(vec_a, vec_b))
#     magnitude_a = sum( a ** 2 for a in vec_a) ** 0.5
#     magnitude_b = sum( b ** 2 for b in vec_b) ** 0.5'

#     if magnitude_a == 0 or magnitude_b == 0:
#         return 0.0
#     return dot_product / (magnitude_a * magnitude_b)

# texts = {
#     "cooking": "How do I cook pasta?",
#     "recipe": "What's the recipe for spaghetti?",
#     "quantum": "Explain quantum computing",
#     "weather": "What's the weather like today?",
# }

# vectors = {name: embeddings.embed_query(text) for name, text in texts.items()}

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0.2,
)

messages = [
    SystemMessage(content = "You are a pirate. Respond in pirate speak. Keep it under 2 sentences."),
    HumanMessage(content= "What is the weather like today?")
]

conversation = [
    SystemMessage(content= "You are a helpful math tutor. Be concise."),
    HumanMessage(content = "What is 2+2?"),
    AIMessage(content= "4"),
    HumanMessage(content = "Now multiply that by 3")
]

response = llm.invoke(conversation)
print(response.content)

prompt = ChatPromptTemplate.from_template("Explain {topic} in one sentence.")

result = prompt.invoke({"topic" : "gravity"})

print(result.messages)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {subject}. Explain things at a {level} level. Be concise."),
    ("human", "{question}")
])

messages = prompt.invoke({
    "subject" : "astronomy",
    "level": "beginner",
    "question" : "Why do stars twinkle?"
})

for msg in messages.to_messages:
    print(msg.content)