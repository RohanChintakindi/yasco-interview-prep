"""
=====================================================
 CHAPTER 3: OUTPUT PARSERS & STRUCTURED OUTPUT
=====================================================

THE PROBLEM
-----------
In Chapter 2, we built chains like: prompt | llm
The LLM returns an AIMessage, and we access .content to get the text.

But what if you need more than raw text? What if your app needs:
  - A JSON object to store in a database?
  - A Python dict to pass to another function?
  - A typed object with specific fields (name, age, score)?

If you ask the LLM "give me JSON", it MIGHT return valid JSON...
or it might wrap it in ```json``` markdown, or add some explanation text,
or return slightly malformed JSON. Raw text is unreliable.

Output parsers solve this:
  1. They tell the LLM what format to respond in (via format instructions)
  2. They parse the LLM's response into the right Python type


THE SOLUTION: OUTPUT PARSERS
-----------------------------
An output parser is (you guessed it) a Runnable.
  Input:  AIMessage (the LLM's response)
  Output: Whatever type you want (str, dict, list, Pydantic object)

It goes at the END of your chain:
  prompt | llm | output_parser


HOW TO RUN THIS FILE:
  pip install pydantic  (you probably already have this)
  python ch3_output_parsers.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="grok-4-1-fast-non-reasoning",
    base_url="https://api.x.ai/v1",
    temperature=0.2,
)


# =============================================================================
# PART 1: StrOutputParser - THE SIMPLEST PARSER
# =============================================================================
#
# What it does: AIMessage -> string
# That's it. It just pulls out the .content field.
#
# Why not just do response.content yourself?
# Because in a CHAIN, you need a Runnable to do it. You can't write
# .content in a pipe. StrOutputParser is the Runnable version of .content.
#
# Without parser:  prompt | llm                 -> returns AIMessage
# With parser:     prompt | llm | StrOutputParser() -> returns str

print("=" * 60)
print("PART 1: StrOutputParser")
print("=" * 60)

# Without StrOutputParser:
chain_no_parser = ChatPromptTemplate.from_template("What is {topic}?") | llm
result = chain_no_parser.invoke({"topic": "gravity"})
print(f"Without parser: {type(result)} -> need result.content to get text")
print()

# With StrOutputParser:
chain_with_parser = ChatPromptTemplate.from_template("What is {topic}?") | llm | StrOutputParser()
result = chain_with_parser.invoke({"topic": "gravity"})
print(f"With parser: {type(result)} -> it's already a string!")
print(f"Result: {result}")
print()

# StrOutputParser is the most common parser. You'll use it in almost every chain.


# =============================================================================
# PART 2: JsonOutputParser - GETTING JSON BACK
# =============================================================================
#
# What it does: AIMessage -> Python dict or list
#
# It works by:
#   1. Providing format_instructions that tell the LLM to respond in JSON
#   2. Parsing the LLM's text response into a Python dict
#
# This is useful when you need structured data to work with in code.

print("=" * 60)
print("PART 2: JsonOutputParser")
print("=" * 60)

json_parser = JsonOutputParser()

# The parser can generate instructions that tell the LLM how to format:
print(f"Format instructions: {json_parser.get_format_instructions()}")
print()

# We include these instructions in our prompt:
prompt = ChatPromptTemplate.from_template(
    "Give me 3 programming languages with their year of creation.\n"
    "Return as a JSON list of objects with 'name' and 'year' keys.\n"
    "{format_instructions}"
)

chain = prompt | llm | json_parser

result = chain.invoke({
    "format_instructions": json_parser.get_format_instructions()
})

print(f"Type: {type(result)}")  # list or dict
print(f"Result: {result}")
print()

# Now you can use this as normal Python data:
if isinstance(result, list):
    for lang in result:
        print(f"  {lang['name']} was created in {lang['year']}")
print()

# The key thing: the result is a PYTHON OBJECT, not a string.
# You can index into it, loop over it, pass it to functions, etc.


# =============================================================================
# PART 3: PYDANTIC & .with_structured_output() - THE BEST APPROACH
# =============================================================================
#
# JsonOutputParser works, but it's loose - you ask for JSON and hope for
# the best. What if a field is missing? What if the types are wrong?
#
# The modern, better approach is .with_structured_output():
#   1. You define a Pydantic model (a Python class that describes your data)
#   2. LangChain forces the LLM to match that EXACT structure
#   3. You get back a typed Python object, not a dict
#
# WHAT IS PYDANTIC?
# -----------------
# Pydantic is a Python library for data validation. You define a class
# with typed fields, and Pydantic ensures the data matches those types.
#
#   class User(BaseModel):
#       name: str
#       age: int
#       email: str
#
# This says: a User MUST have a name (string), age (integer), and email (string).
# If you try to create a User with age="twenty", Pydantic throws an error.
#
# LangChain uses this: you define the shape, the LLM fills it in.

print("=" * 60)
print("PART 3: Pydantic Structured Output")
print("=" * 60)


# Step 1: Define the structure you want back
class MovieReview(BaseModel):
    """A review of a movie."""
    title: str = Field(description="The movie title")
    rating: int = Field(description="Rating from 1 to 10")
    summary: str = Field(description="One sentence summary of the movie")
    recommend: bool = Field(description="Whether you would recommend this movie")

# Let's break this down:
#   class MovieReview(BaseModel):  -> This is a Pydantic model
#   title: str                     -> Must have a title, must be a string
#   Field(description="...")       -> Tells the LLM what this field means
#                                     (the LLM reads these descriptions!)

# Step 2: Create a structured LLM
# .with_structured_output() wraps the LLM so it always returns your model
structured_llm = llm.with_structured_output(MovieReview)

# Step 3: Use it like a normal LLM
result = structured_llm.invoke("Give me a review of The Dark Knight")

# result is a MovieReview object, NOT an AIMessage, NOT a string
print(f"Type: {type(result)}")
print(f"Title: {result.title}")
print(f"Rating: {result.rating}/10")
print(f"Summary: {result.summary}")
print(f"Recommend: {result.recommend}")
print()

# This is SO much better than parsing raw text:
#   - Guaranteed structure (no missing fields)
#   - Correct types (rating is an int, not "8/10" string)
#   - IDE autocomplete works (result.title, result.rating)
#   - No regex or string parsing needed


# =============================================================================
# PART 4: STRUCTURED OUTPUT IN A CHAIN
# =============================================================================
#
# You can combine structured output with prompt templates.
# This is extremely powerful for building real applications.

print("=" * 60)
print("PART 4: Structured Output in a Chain")
print("=" * 60)


class CountryInfo(BaseModel):
    """Information about a country."""
    name: str = Field(description="The country name")
    capital: str = Field(description="The capital city")
    population: str = Field(description="Approximate population")
    languages: list[str] = Field(description="List of official languages")
    fun_fact: str = Field(description="An interesting fact about this country")


# The chain: template -> structured LLM
# Note: we put .with_structured_output() on the LLM, not as a separate step
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a geography expert. Provide accurate, factual information."),
    ("human", "Tell me about {country}"),
])

chain = prompt | llm.with_structured_output(CountryInfo)

result = chain.invoke({"country": "Japan"})

print(f"Country: {result.name}")
print(f"Capital: {result.capital}")
print(f"Population: {result.population}")
print(f"Languages: {', '.join(result.languages)}")
print(f"Fun fact: {result.fun_fact}")
print()

# You can now easily store this in a database, display in a UI,
# or pass to another function. The data is clean and typed.


# =============================================================================
# PART 5: MULTIPLE ITEMS (LISTS OF STRUCTURED DATA)
# =============================================================================
#
# What if you want a LIST of structured objects?

print("=" * 60)
print("PART 5: Lists of Structured Data")
print("=" * 60)


class Book(BaseModel):
    """A book recommendation."""
    title: str = Field(description="The book title")
    author: str = Field(description="The author's name")
    why: str = Field(description="Why this book is recommended, in one sentence")


class BookList(BaseModel):
    """A list of book recommendations."""
    books: list[Book] = Field(description="List of recommended books")


chain = (
    ChatPromptTemplate.from_template("Recommend 3 books about {topic}")
    | llm.with_structured_output(BookList)
)

result = chain.invoke({"topic": "artificial intelligence"})

for i, book in enumerate(result.books, 1):
    print(f"  {i}. '{book.title}' by {book.author}")
    print(f"     Why: {book.why}")
print()


# =============================================================================
# PART 6: WHEN TO USE WHICH PARSER
# =============================================================================
#
# StrOutputParser:
#   Use when: You just need the text response as a string
#   Example: chatbot responses, explanations, summaries
#   This is the most common one.
#
# JsonOutputParser:
#   Use when: You need a dict/list but don't want to define a Pydantic model
#   Example: quick prototyping, flexible schemas
#   Less reliable than Pydantic.
#
# .with_structured_output(PydanticModel):
#   Use when: You need guaranteed structure with specific fields and types
#   Example: extracting data, building APIs, database insertion
#   THE BEST option for production apps. Use this whenever possible.
#
#
# MENTAL MODEL:
#   Raw LLM response:  "The capital of France is Paris, with a population of..."
#   StrOutputParser:    "The capital of France is Paris, with a population of..."
#   JsonOutputParser:   {"capital": "Paris", "population": "67 million"}
#   Pydantic:           CountryInfo(capital="Paris", population="67 million")
#
#   Each one gives you more structure and reliability.


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# String output:
#   chain = prompt | llm | StrOutputParser()
#   result = chain.invoke({...})  # -> str
#
# JSON output:
#   parser = JsonOutputParser()
#   chain = prompt | llm | parser
#   result = chain.invoke({..., "format_instructions": parser.get_format_instructions()})
#
# Structured (Pydantic) output:
#   class MyModel(BaseModel):
#       field: type = Field(description="what this is")
#
#   chain = prompt | llm.with_structured_output(MyModel)
#   result = chain.invoke({...})  # -> MyModel instance
#
# =============================================================================
