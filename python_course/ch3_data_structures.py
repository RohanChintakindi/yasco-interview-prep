"""
=====================================================
 CHAPTER 3: DATA STRUCTURES - LISTS, DICTS, TUPLES, SETS
=====================================================

Variables hold ONE value. But what if you need to store MANY values?
  - A list of student names
  - A mapping of country -> capital
  - A set of unique tags

Python has 4 built-in collection types:

  LIST:   Ordered, mutable, allows duplicates      [1, 2, 3]
  DICT:   Key-value pairs, mutable                 {"a": 1, "b": 2}
  TUPLE:  Ordered, IMMUTABLE, allows duplicates    (1, 2, 3)
  SET:    Unordered, mutable, NO duplicates        {1, 2, 3}


HOW TO RUN:
  python ch3_data_structures.py
"""

# =============================================================================
# PART 1: LISTS - ORDERED, MUTABLE COLLECTIONS
# =============================================================================
#
# Lists are the most-used data structure. They hold items in ORDER
# and you can add, remove, or change items.

print("=" * 40)
print("PART 1: Lists")
print("=" * 40)

# Creating lists:
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]  # Can mix types
empty = []

# Accessing items (0-indexed):
print(f"First: {fruits[0]}")     # apple
print(f"Last: {fruits[-1]}")     # cherry (negative = from end)
print(f"Slice: {numbers[1:4]}")  # [2, 3, 4] (index 1 to 3)

# Modifying:
fruits.append("date")            # Add to end
fruits.insert(1, "avocado")      # Insert at position 1
print(f"After add: {fruits}")

fruits.remove("banana")          # Remove by value
popped = fruits.pop()            # Remove & return last item
print(f"After remove: {fruits}, popped: {popped}")

# Useful operations:
print(f"Length: {len(fruits)}")
print(f"'apple' in fruits: {'apple' in fruits}")
print(f"Sorted numbers: {sorted([3, 1, 4, 1, 5])}")
print(f"Reversed: {list(reversed(fruits))}")

# List methods:
nums = [3, 1, 4, 1, 5, 9]
nums.sort()                      # Sort IN PLACE (modifies the list)
print(f"Sorted: {nums}")
print(f"Count of 1: {nums.count(1)}")
print(f"Index of 5: {nums.index(5)}")
print()


# =============================================================================
# PART 2: DICTIONARIES - KEY-VALUE PAIRS
# =============================================================================
#
# Dicts map KEYS to VALUES. Like a phone book: name -> number.
# Keys must be unique. Values can be anything.

print("=" * 40)
print("PART 2: Dictionaries")
print("=" * 40)

# Creating dicts:
person = {
    "name": "Chint",
    "age": 25,
    "languages": ["Python", "JavaScript"],
    "is_student": True,
}

# Accessing values:
print(f"Name: {person['name']}")
print(f"Age: {person.get('age')}")         # .get() is safer
print(f"Job: {person.get('job', 'N/A')}")  # Returns 'N/A' if key missing

# Modifying:
person["age"] = 26                # Update existing key
person["city"] = "New York"       # Add new key
del person["is_student"]          # Delete a key
print(f"Updated: {person}")

# Iterating:
print("\nAll keys and values:")
for key, value in person.items():
    print(f"  {key}: {value}")

# Useful operations:
print(f"\nKeys: {list(person.keys())}")
print(f"Values: {list(person.values())}")
print(f"'name' in person: {'name' in person}")
print(f"Length: {len(person)}")
print()

# NESTED DICTS (dicts inside dicts):
students = {
    "chint": {"grade": "A", "score": 95},
    "alice": {"grade": "B", "score": 82},
}
print(f"Chint's score: {students['chint']['score']}")
print()


# =============================================================================
# PART 3: TUPLES - IMMUTABLE SEQUENCES
# =============================================================================
#
# Tuples are like lists but IMMUTABLE (can't be changed after creation).
# Use them for data that shouldn't change: coordinates, RGB colors, etc.

print("=" * 40)
print("PART 3: Tuples")
print("=" * 40)

# Creating:
point = (3, 4)
rgb = (255, 128, 0)
single = (42,)     # Note the comma! (42) is just 42, (42,) is a tuple

print(f"Point: {point}, x={point[0]}, y={point[1]}")
print(f"RGB: {rgb}")

# Tuple unpacking (super useful!):
x, y = point
print(f"Unpacked: x={x}, y={y}")

# Swap variables:
a, b = 1, 2
a, b = b, a
print(f"Swapped: a={a}, b={b}")

# Functions that return multiple values use tuples:
def get_name_and_age():
    return "Chint", 25

name, age = get_name_and_age()
print(f"{name} is {age}")

# Can't modify:
# point[0] = 5  # ERROR! Tuples are immutable
print()


# =============================================================================
# PART 4: SETS - UNIQUE, UNORDERED COLLECTIONS
# =============================================================================
#
# Sets only store UNIQUE values. Adding a duplicate does nothing.
# Great for removing duplicates and set operations (union, intersection).

print("=" * 40)
print("PART 4: Sets")
print("=" * 40)

# Creating:
colors = {"red", "green", "blue"}
numbers = {1, 2, 2, 3, 3, 3}  # Duplicates are ignored!
print(f"Colors: {colors}")
print(f"Numbers (dupes removed): {numbers}")

# Remove duplicates from a list:
dupes = [1, 2, 2, 3, 3, 4]
unique = list(set(dupes))
print(f"Unique: {unique}")

# Adding / removing:
colors.add("yellow")
colors.discard("red")       # Remove (no error if missing)
print(f"Updated colors: {colors}")

# Set operations:
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(f"Union (all):        {a | b}")          # {1,2,3,4,5,6}
print(f"Intersection (both): {a & b}")         # {3,4}
print(f"Difference (a not b): {a - b}")        # {1,2}
print(f"Symmetric diff:      {a ^ b}")         # {1,2,5,6}

print(f"Is 3 in a? {3 in a}")
print()


# =============================================================================
# PART 5: LIST COMPREHENSIONS
# =============================================================================
#
# A compact way to create lists. One of Python's most loved features.
#   [expression for item in iterable if condition]

print("=" * 40)
print("PART 5: List Comprehensions")
print("=" * 40)

# Regular loop:
squares = []
for x in range(6):
    squares.append(x ** 2)
print(f"Squares (loop): {squares}")

# Same thing, one line:
squares = [x ** 2 for x in range(6)]
print(f"Squares (comprehension): {squares}")

# With a filter:
evens = [x for x in range(10) if x % 2 == 0]
print(f"Evens: {evens}")

# Transform strings:
words = ["hello", "world", "python"]
upper = [w.upper() for w in words]
print(f"Uppercase: {upper}")

# Dict comprehension:
word_lengths = {w: len(w) for w in words}
print(f"Word lengths: {word_lengths}")

# Set comprehension:
first_letters = {w[0] for w in words}
print(f"First letters: {first_letters}")
print()


# =============================================================================
# PART 6: WHEN TO USE WHICH
# =============================================================================
#
# LIST:  Ordered collection, may have duplicates
#        Use for: shopping lists, search results, sequences
#
# DICT:  Key-value lookup
#        Use for: user profiles, config, JSON-like data, counting
#
# TUPLE: Immutable sequence
#        Use for: coordinates, function return values, dict keys
#
# SET:   Unique values, fast membership testing
#        Use for: removing duplicates, tags, "have we seen this?"


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# List:  [1,2,3]   .append() .remove() .pop() .sort() len() in
# Dict:  {"a":1}   .get() .keys() .values() .items() del d[k] in
# Tuple: (1,2,3)   indexing, unpacking (immutable)
# Set:   {1,2,3}   .add() .discard() | & - ^ in
#
# Comprehension: [expr for x in iter if cond]
#
# =============================================================================
