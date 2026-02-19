"""
=====================================================
 CHAPTER 7: ADVANCED FEATURES
=====================================================

The features that make Python POWERFUL and ELEGANT.
These show up everywhere in professional Python code.

  - Decorators
  - Generators
  - Context managers
  - Type hints
  - Dataclasses
  - Walrus operator


HOW TO RUN:
  python ch7_advanced_features.py
"""

# =============================================================================
# PART 1: DECORATORS - WRAPPING FUNCTIONS
# =============================================================================
#
# A decorator adds behavior to a function WITHOUT modifying it.
# It's a function that takes a function and returns a new function.
#
# Real-world uses: logging, timing, authentication, caching

print("=" * 40)
print("PART 1: Decorators")
print("=" * 40)

import time
from functools import wraps


def timer(func):
    """Decorator: prints how long a function takes."""
    @wraps(func)  # Preserves original function's name/docstring
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3):
    """Decorator WITH ARGUMENTS: retries a function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator


@timer
def slow_function():
    time.sleep(0.1)
    return "done"


result = slow_function()
print(f"  Result: {result}")
print()

# Stacking decorators:
import random

@timer
@retry(max_attempts=5)
def unreliable():
    """Fails 70% of the time."""
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return "success!"

random.seed(42)
try:
    result = unreliable()
    print(f"  Got: {result}")
except ValueError:
    print("  Failed after all retries")
print()


# =============================================================================
# PART 2: GENERATORS - LAZY SEQUENCES
# =============================================================================
#
# A generator produces values ONE AT A TIME instead of all at once.
# Uses yield instead of return. Memory efficient for large datasets.
#
# List: [1, 2, 3, 4, 5] -> ALL 5 values in memory at once
# Generator: yields 1, then 2, then 3... -> only 1 value in memory at a time

print("=" * 40)
print("PART 2: Generators")
print("=" * 40)


def countdown(n):
    """Generator: yields n, n-1, ..., 1."""
    while n > 0:
        yield n  # Pause here, return n, resume on next call
        n -= 1


print("Countdown:")
for num in countdown(5):
    print(f"  {num}")
print()


# Generator expression (like list comprehension but with ()):
squares_list = [x**2 for x in range(1000000)]  # 1M items in memory!
squares_gen = (x**2 for x in range(1000000))    # Almost no memory!

print(f"List size: {squares_list.__sizeof__()} bytes")
print(f"Generator: {squares_gen.__sizeof__()} bytes (tiny!)")
print()

# Practical: read a huge file line by line
def read_large_file(filepath):
    """Generator that yields one line at a time."""
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


# =============================================================================
# PART 3: CONTEXT MANAGERS
# =============================================================================
#
# The `with` statement ensures cleanup happens even if errors occur.
# You can create your own with __enter__ and __exit__.

print("=" * 40)
print("PART 3: Context managers")
print("=" * 40)


class Timer:
    """Context manager that times a block of code."""
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f"  Block took {self.elapsed:.4f}s")
        return False  # Don't suppress exceptions


with Timer():
    total = sum(range(1000000))
print(f"  Sum: {total}")
print()


# =============================================================================
# PART 4: TYPE HINTS
# =============================================================================
#
# Type hints don't ENFORCE types - they're DOCUMENTATION for humans and tools.
# IDEs use them for autocomplete and error detection.

print("=" * 40)
print("PART 4: Type hints")
print("=" * 40)


def greet(name: str, times: int = 1) -> str:
    """Type hints: name is str, times is int, returns str."""
    return (f"Hello, {name}! " * times).strip()


def process_items(items: list[str]) -> dict[str, int]:
    """Returns a dict mapping each item to its length."""
    return {item: len(item) for item in items}


print(greet("Chint", 2))
print(process_items(["apple", "banana", "cherry"]))
print()

# Common type hints:
# str, int, float, bool
# list[str], dict[str, int], tuple[int, int]
# Optional[str] = str | None
# Union[str, int] = str or int (modern: str | int)


# =============================================================================
# PART 5: DATACLASSES
# =============================================================================
#
# Dataclasses auto-generate __init__, __repr__, __eq__, etc.
# Perfect for classes that are mainly data containers.

print("=" * 40)
print("PART 5: Dataclasses")
print("=" * 40)

from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    email: str
    age: int
    tags: list[str] = field(default_factory=list)

    # __init__, __repr__, __eq__ are auto-generated!


u1 = User("Chint", "chint@example.com", 25)
u2 = User("Chint", "chint@example.com", 25)
u3 = User("Alice", "alice@example.com", 22, tags=["admin"])

print(f"u1: {u1}")            # Auto __repr__
print(f"u1 == u2: {u1 == u2}")  # Auto __eq__: True
print(f"u3 tags: {u3.tags}")
print()


# =============================================================================
# PART 6: USEFUL ONE-LINERS
# =============================================================================

print("=" * 40)
print("PART 6: Useful patterns")
print("=" * 40)

# Walrus operator (:=) - assign and use in one expression:
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
if (n := len(data)) > 5:
    print(f"List has {n} items (that's a lot!)")

# Unpacking:
first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")

# Dictionary merge (Python 3.9+):
defaults = {"color": "blue", "size": "medium"}
custom = {"size": "large", "weight": "heavy"}
merged = defaults | custom  # custom overrides defaults
print(f"Merged: {merged}")

# Conditional expression:
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Status: {status}")

# any() / all():
numbers = [2, 4, 6, 8]
print(f"All even? {all(n % 2 == 0 for n in numbers)}")
print(f"Any > 5?  {any(n > 5 for n in numbers)}")
print()


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Decorator:
#   def my_decorator(func):
#       @wraps(func)
#       def wrapper(*a, **kw): ...; return func(*a, **kw)
#       return wrapper
#   @my_decorator
#   def my_func(): ...
#
# Generator:
#   def gen(): yield value
#   (expr for x in iterable)
#
# Type hints:
#   def f(x: int, y: str = "hi") -> bool: ...
#
# Dataclass:
#   @dataclass
#   class Foo:
#       x: int
#       y: str = "default"
#
# Walrus:     if (n := len(x)) > 5:
# Unpack:     first, *rest = [1,2,3]
# Dict merge: d1 | d2
#
# =============================================================================
