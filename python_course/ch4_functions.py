"""
=====================================================
 CHAPTER 4: FUNCTIONS
=====================================================

WHAT IS A FUNCTION?
-------------------
A function is a reusable block of code with a name.
Instead of writing the same code over and over, you write it ONCE
as a function and CALL it whenever you need it.

  Without functions:        With functions:
    print("Hello Chint")      def greet(name):
    print("Hello Alice")          print(f"Hello {name}")
    print("Hello Bob")
                              greet("Chint")
                              greet("Alice")
                              greet("Bob")

Functions make code:
  - REUSABLE (write once, use many times)
  - READABLE (greet("Chint") is clearer than 5 lines of code)
  - TESTABLE (you can test a function in isolation)
  - ORGANIZED (break big problems into small pieces)


HOW TO RUN:
  python ch4_functions.py
"""

# =============================================================================
# PART 1: BASIC FUNCTIONS
# =============================================================================
#
# def function_name(parameters):
#     """Docstring: what this function does."""
#     code...
#     return value

print("=" * 40)
print("PART 1: Basic functions")
print("=" * 40)


def greet(name):
    """Print a greeting for the given name."""
    print(f"Hello, {name}!")


# CALLING the function:
greet("Chint")
greet("Alice")
print()


# Functions that RETURN values:
def add(a, b):
    """Return the sum of a and b."""
    return a + b


result = add(3, 4)
print(f"3 + 4 = {result}")

# Return can be used in expressions:
print(f"10 + 20 = {add(10, 20)}")
print()


# Multiple return values (returns a tuple):
def min_max(numbers):
    """Return both the minimum and maximum of a list."""
    return min(numbers), max(numbers)


lo, hi = min_max([4, 2, 9, 1, 7])
print(f"Min: {lo}, Max: {hi}")
print()


# =============================================================================
# PART 2: PARAMETERS & ARGUMENTS
# =============================================================================

print("=" * 40)
print("PART 2: Parameters & Arguments")
print("=" * 40)


# DEFAULT PARAMETERS: used if no argument is provided
def greet_with_default(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet_with_default("Chint")                  # Uses default: "Hello, Chint!"
greet_with_default("Chint", "Hey")           # Override: "Hey, Chint!"
greet_with_default("Chint", greeting="Yo")   # Keyword argument
print()


# KEYWORD ARGUMENTS: specify by name (order doesn't matter)
def create_profile(name, age, city="Unknown"):
    return f"{name}, age {age}, from {city}"

print(create_profile("Chint", 25, "NYC"))
print(create_profile(age=25, city="NYC", name="Chint"))  # Any order!
print()


# *args: accept ANY NUMBER of positional arguments
def sum_all(*numbers):
    """Sum any number of arguments."""
    return sum(numbers)

print(f"sum_all(1, 2, 3): {sum_all(1, 2, 3)}")
print(f"sum_all(10, 20): {sum_all(10, 20)}")
print()


# **kwargs: accept ANY NUMBER of keyword arguments
def print_info(**kwargs):
    """Print all keyword arguments."""
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print("print_info(name='Chint', age=25):")
print_info(name="Chint", age=25, lang="Python")
print()


# =============================================================================
# PART 3: SCOPE - WHERE VARIABLES LIVE
# =============================================================================
#
# Variables inside a function are LOCAL - they only exist inside that function.
# Variables outside are GLOBAL - they exist everywhere.

print("=" * 40)
print("PART 3: Scope")
print("=" * 40)

x = "global"  # Global variable

def my_function():
    x = "local"  # Local variable (different from global x!)
    print(f"  Inside function: x = {x}")

my_function()
print(f"  Outside function: x = {x}")  # Still "global"!
print()


# =============================================================================
# PART 4: LAMBDA FUNCTIONS (ANONYMOUS FUNCTIONS)
# =============================================================================
#
# Small, one-line functions without a name.
# Useful for quick operations, especially with sort/map/filter.
#
# lambda arguments: expression

print("=" * 40)
print("PART 4: Lambda functions")
print("=" * 40)

# Regular function:
def double(x):
    return x * 2

# Same thing as lambda:
double_lambda = lambda x: x * 2

print(f"double(5) = {double(5)}")
print(f"lambda(5) = {double_lambda(5)}")

# Common use: sorting by a custom key
students = [("Alice", 85), ("Bob", 92), ("Chint", 78)]
students.sort(key=lambda s: s[1])  # Sort by score (index 1)
print(f"Sorted by score: {students}")

# Sort dicts by a key:
people = [{"name": "Chint", "age": 25}, {"name": "Alice", "age": 22}]
people.sort(key=lambda p: p["age"])
print(f"Sorted by age: {people}")
print()


# =============================================================================
# PART 5: HIGHER-ORDER FUNCTIONS (map, filter, zip)
# =============================================================================

print("=" * 40)
print("PART 5: map, filter, zip")
print("=" * 40)

# map: apply a function to every item
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(f"Doubled: {doubled}")

# filter: keep items that pass a test
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")

# zip: combine two lists into pairs
names = ["Chint", "Alice", "Bob"]
scores = [95, 82, 88]
paired = list(zip(names, scores))
print(f"Zipped: {paired}")

# (List comprehensions often replace map/filter:)
doubled2 = [x * 2 for x in numbers]  # Same as map above
evens2 = [x for x in numbers if x % 2 == 0]  # Same as filter
print()


# =============================================================================
# PART 6: DECORATORS (PREVIEW)
# =============================================================================
#
# A decorator is a function that WRAPS another function.
# We'll go deeper in Ch7, but here's a taste.

print("=" * 40)
print("PART 6: Decorators (preview)")
print("=" * 40)

import time

def timer(func):
    """Decorator that measures execution time."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_add(a, b):
    time.sleep(0.1)  # Simulate slow operation
    return a + b

result = slow_add(3, 4)
print(f"  Result: {result}")
print()


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Define:     def name(params):
# Return:     return value
# Default:    def f(x, y=10):
# *args:      def f(*args):     -> tuple of positional args
# **kwargs:   def f(**kwargs):  -> dict of keyword args
# Lambda:     lambda x: x * 2
# Decorator:  @decorator_name above def
#
# =============================================================================
