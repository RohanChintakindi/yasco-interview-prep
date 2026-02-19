"""
==============================================
 CHAPTER 2: MESSAGES & PROMPT TEMPLATES
==============================================

THE BIG PICTURE
---------------
In Chapter 1, we passed a plain string to the LLM:
  llm.invoke("What is Python?")

But that's actually a shortcut. Under the hood, LLMs don't work with
plain text - they work with MESSAGES. Each message has a ROLE that tells
the model who's talking.

Think of it like a play script:

  DIRECTOR: You are a helpful assistant that speaks like a pirate.
  USER: What's the weather like?
  ASSISTANT: Arrr, it be sunny with a chance of scallywags, matey!

The "director" is the SYSTEM message - instructions the user doesn't see.
The "user" is the HUMAN message - what the person is asking.
The "assistant" is the AI message - the model's response.

This role system is HOW you control the model's behavior, personality,
and constraints. It's the difference between a generic chatbot and one
that actually does what you want.


WHY PROMPT TEMPLATES?
---------------------
Imagine you're building a translation app. You need prompts like:
  "Translate '{text}' from {source_lang} to {target_lang}"

You COULD use Python f-strings:
  f"Translate '{text}' from {source_lang} to {target_lang}"

But LangChain templates are better because:
  1. They're Runnables - they plug into chains with |
  2. They handle message roles (system/human/ai)
  3. They validate that you provided all required variables
  4. They can include dynamic conversation history


HOW TO RUN THIS FILE:
  python ch2_messages_and_prompts.py
"""

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


# =============================================================================
# PART 1: THE THREE MESSAGE TYPES
# =============================================================================
#
# Every conversation with a chat model is a LIST of messages.
# Each message has a role:
#
# SystemMessage (role: "system")
#   - Instructions for the AI that the user doesn't write
#   - Sets personality, rules, constraints, format requirements
#   - Example: "You are a Spanish tutor. Only respond in Spanish."
#   - The model treats this as its "programming" - it follows these rules
#   - Always put this FIRST in the message list
#
# HumanMessage (role: "user")
#   - What the human is saying/asking
#   - This is the actual question or request
#   - Example: "How do I say 'hello' in Spanish?"
#
# AIMessage (role: "assistant")
#   - The model's previous responses
#   - You include these to give the model MEMORY of past conversation
#   - Example: "'Hello' in Spanish is 'Hola'."
#   - You don't write these yourself usually - the model generates them
#   - But you DO include past ones to maintain conversation context

print("=" * 60)
print("PART 1: The Three Message Types")
print("=" * 60)

messages = [
    SystemMessage(content="You are a pirate. Respond in pirate speak. Keep it under 2 sentences."),
    HumanMessage(content="What is the weather like today?"),
]

response = llm.invoke(messages)
print(f"Pirate says: {response.content}")
print()

# Now watch what happens WITHOUT the system message:
messages_no_system = [
    HumanMessage(content="What is the weather like today?"),
]

response = llm.invoke(messages_no_system)
print(f"Normal AI says: {response.content}")
print()

# See the difference? The SystemMessage completely changed the behavior.
# This is the #1 tool for controlling AI behavior.


# =============================================================================
# PART 2: HOW CONVERSATION MEMORY WORKS
# =============================================================================
#
# This is a concept that confuses many beginners:
#
#   ** LLMs have NO memory. They are stateless. **
#
# Every time you call .invoke(), the model sees the conversation fresh.
# It doesn't remember what you said 5 seconds ago.
#
# So how does ChatGPT "remember" your conversation? Simple:
# The app sends the ENTIRE conversation history with every request.
#
# Request 1: [HumanMessage("My name is Chint")]
# Request 2: [HumanMessage("My name is Chint"),
#              AIMessage("Nice to meet you, Chint!"),
#              HumanMessage("What's my name?")]
#
# The model doesn't "remember" your name. It sees it right there in
# the message list. If you DON'T include the history, it won't know.

print("=" * 60)
print("PART 2: Conversation Memory (it's an illusion!)")
print("=" * 60)

# Multi-turn conversation: we manually include the history
conversation = [
    SystemMessage(content="You are a helpful math tutor. Be concise."),
    HumanMessage(content="What is 2 + 2?"),
    AIMessage(content="4"),                          # We provide the AI's past answer
    HumanMessage(content="Now multiply that by 3"),  # "that" = 4 (model can see it above)
]

response = llm.invoke(conversation)
print(f"Math tutor says: {response.content}")  # Should say 12
print()

# Without the history, "that" would make no sense:
no_context = [
    HumanMessage(content="Now multiply that by 3"),  # Multiply WHAT by 3??
]

response = llm.invoke(no_context)
print(f"Without context: {response.content}")  # Won't know what "that" refers to
print()

# KEY INSIGHT:
# "Memory" in AI apps is just "send the old messages every time."
# This costs tokens (= money), which is why apps often trim old history.


# =============================================================================
# PART 3: ChatPromptTemplate - YOUR FIRST TEMPLATE
# =============================================================================
#
# Writing message lists by hand gets tedious fast. Prompt templates let
# you create REUSABLE prompts with {variables} that get filled in later.
#
# A ChatPromptTemplate is:
#   1. A Runnable (has .invoke(), .stream(), etc.)
#   2. Takes a dict of variables as input
#   3. Outputs a list of formatted messages
#
# The simplest version:

print("=" * 60)
print("PART 3: ChatPromptTemplate.from_template()")
print("=" * 60)

# from_template() creates a single HumanMessage with a variable
prompt = ChatPromptTemplate.from_template("Explain {topic} in one sentence.")

# This is a Runnable. Let's call .invoke() on it:
result = prompt.invoke({"topic": "gravity"})

# What does it output? A list of messages!
print(f"Type: {type(result)}")
print(f"Messages: {result.messages}")
print()

# It created: [HumanMessage(content="Explain gravity in one sentence.")]
# The {topic} was replaced with "gravity".

# IMPORTANT: from_template() ONLY creates a HumanMessage.
# There's no system message. This is fine for simple prompts,
# but usually you want more control. That's where from_messages() comes in.


# =============================================================================
# PART 4: ChatPromptTemplate.from_messages() - FULL CONTROL
# =============================================================================
#
# from_messages() lets you define the EXACT structure of your prompt:
# which messages, what roles, which parts are variables.
#
# You use TUPLES: (role, content)
#   ("system", "...")   -> SystemMessage
#   ("human", "...")    -> HumanMessage
#   ("ai", "...")       -> AIMessage

print("=" * 60)
print("PART 4: from_messages() - Full control over message structure")
print("=" * 60)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {subject}. Explain things at a {level} level. Be concise."),
    ("human", "{question}"),
])

# This template has THREE variables: subject, level, question
# Let's fill them in:
messages = prompt.invoke({
    "subject": "astronomy",
    "level": "beginner",
    "question": "Why do stars twinkle?",
})

print("Generated messages:")
for msg in messages.messages:
    print(f"  [{msg.type}]: {msg.content}")
print()

# Now send to the LLM
response = llm.invoke(messages)
print(f"Answer: {response.content}")
print()

# Let's reuse the SAME template with different inputs:
messages = prompt.invoke({
    "subject": "astronomy",
    "level": "PhD researcher",
    "question": "Why do stars twinkle?",
})

response = llm.invoke(messages)
print(f"PhD-level answer: {response.content}")
print()

# Same question, completely different answer - just by changing a variable!
# This is the power of templates: one template, infinite variations.


# =============================================================================
# PART 5: MAKING YOUR FIRST CHAIN (PREVIEW)
# =============================================================================
#
# Remember: both `prompt` and `llm` are Runnables.
# Runnables can be connected with the | pipe operator.
#
#   prompt | llm
#
# This creates a NEW Runnable (a chain) where:
#   1. prompt receives a dict -> outputs messages
#   2. llm receives those messages -> outputs AIMessage
#
# The output of the LEFT side flows into the input of the RIGHT side.
# Just like Unix pipes: cat file.txt | grep "hello" | wc -l

print("=" * 60)
print("PART 5: Your first chain (prompt | llm)")
print("=" * 60)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a comedian. Tell short jokes."),
    ("human", "Tell me a joke about {topic}"),
])

# WITHOUT a chain (manual, two steps):
messages = prompt.invoke({"topic": "programming"})
response = llm.invoke(messages)
print(f"Manual: {response.content}")
print()

# WITH a chain (one step):
chain = prompt | llm
response = chain.invoke({"topic": "programming"})
print(f"Chain: {response.content}")
print()

# Same result, but the chain version is:
#   - Cleaner to read
#   - Reusable
#   - Can be extended: prompt | llm | parser | next_step | ...


# =============================================================================
# PART 6: MessagesPlaceholder - DYNAMIC CONVERSATION HISTORY
# =============================================================================
#
# Here's a common scenario: you're building a chatbot and need to include
# past conversation in the prompt. But the history changes every turn -
# it could be 0 messages or 50 messages.
#
# You can't hardcode this in a template. You need a PLACEHOLDER that
# says "insert a variable number of messages here."
#
# That's MessagesPlaceholder.

print("=" * 60)
print("PART 6: MessagesPlaceholder - Dynamic chat history")
print("=" * 60)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Be concise."),
    MessagesPlaceholder(variable_name="chat_history"),  # <- 0 to N messages go here
    ("human", "{question}"),
])

# Simulate a conversation that's been going for a few turns:
history = [
    HumanMessage(content="My name is Chint"),
    AIMessage(content="Nice to meet you, Chint! How can I help?"),
    HumanMessage(content="I'm learning LangChain"),
    AIMessage(content="Great choice! It's a powerful framework for building AI apps."),
]

messages = prompt.invoke({
    "chat_history": history,
    "question": "What's my name and what am I learning?",
})

response = llm.invoke(messages)
print(f"Response: {response.content}")
print()

# The model can answer because it sees the full history.
# In a real chatbot, you'd append new messages to the history list
# after each turn and pass it back each time.

# Empty history works too (first message in a conversation):
messages = prompt.invoke({
    "chat_history": [],
    "question": "Hello, who are you?",
})

response = llm.invoke(messages)
print(f"First message (no history): {response.content}")
print()


# =============================================================================
# PART 7: PUTTING IT ALL TOGETHER
# =============================================================================
#
# Let's build a mini chatbot using everything from this chapter:
# System message + history + user input, all in a chain.

print("=" * 60)
print("PART 7: Mini chatbot (combining everything)")
print("=" * 60)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly coding tutor. Keep answers to 1-2 sentences."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm  # This is a Runnable!

# Simulate a 3-turn conversation:
history = []

questions = [
    "What is a variable in Python?",
    "Can you give me an example?",
    "What if I want to store a number instead?",
]

for question in questions:
    response = chain.invoke({"history": history, "input": question})
    print(f"You: {question}")
    print(f"AI:  {response.content}")
    print()

    # Add this exchange to history for next turn
    history.append(HumanMessage(content=question))
    history.append(AIMessage(content=response.content))


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Message types:
#   SystemMessage(content="...")  or  ("system", "...")
#   HumanMessage(content="...")   or  ("human", "...")
#   AIMessage(content="...")      or  ("ai", "...")
#
# Simple template (human message only):
#   prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
#
# Full template (with roles):
#   prompt = ChatPromptTemplate.from_messages([
#       ("system", "You are {role}"),
#       ("human", "{question}"),
#   ])
#
# Template with chat history:
#   prompt = ChatPromptTemplate.from_messages([
#       ("system", "You are helpful."),
#       MessagesPlaceholder(variable_name="history"),
#       ("human", "{input}"),
#   ])
#
# Using a template:
#   messages = prompt.invoke({"topic": "...", ...})
#
# Chain:
#   chain = prompt | llm
#   response = chain.invoke({"topic": "..."})
#
# =============================================================================
