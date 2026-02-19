"""
=====================================================
 PYTHON INTERVIEW PREP — JUNIOR DEV / INTERN LEVEL
=====================================================

This file has TWO modes:

  1. STUDY GUIDE  — Read through 30 questions with detailed answers.
                    Covers everything a junior dev interview would ask.

  2. INTERACTIVE QUIZ — Run this file and answer questions in your terminal.
                         Get scored at the end with feedback.


HOW TO RUN:
  python interview_python_basics.py          (interactive quiz)
  python interview_python_basics.py study    (print study guide)


TOPICS COVERED:
  Round 1 (Easy)    — Variables, types, strings, basic operations
  Round 2 (Easy-Med) — Lists, dicts, tuples, sets
  Round 3 (Medium)  — Control flow, loops, comprehensions
  Round 4 (Medium)  — Functions, scope, args/kwargs
  Round 5 (Med-Hard) — OOP: classes, inheritance, dunder methods
  Round 6 (Hard)    — Common gotchas & tricky behavior
  Round 7 (Hard)    — Output prediction (what does this print?)
  Round 8 (Practical) — Bug fixing & code writing
"""

import sys
import textwrap

# =============================================================================
#  ALL QUESTIONS — STUDY GUIDE + QUIZ DATA
# =============================================================================
#
# Each question is a dict with:
#   "id"         — question number
#   "round"      — which round it belongs to
#   "difficulty" — Easy / Medium / Hard
#   "type"       — Conceptual / Output / Bug Fix / Code Writing
#   "question"   — the question text
#   "answer"     — the full, detailed answer (shown in study guide)
#   "short"      — short accepted keywords for interactive quiz grading
#   "code"       — optional code snippet to display

QUESTIONS = [

    # =========================================================================
    # ROUND 1: VARIABLES, TYPES & STRINGS (Easy)
    # =========================================================================

    {
        "id": 1,
        "round": "Round 1: Variables & Types",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What are Python's main built-in data types?",
        "answer": """The main built-in types are:

  Numeric:    int, float, complex
  Text:       str
  Boolean:    bool (True / False)
  Sequence:   list, tuple, range
  Mapping:    dict
  Set:        set, frozenset
  None:       NoneType

In an interview, mentioning int, float, str, bool, list, dict, tuple, set
is usually enough. Bonus points for mentioning NoneType.""",
        "short": ["int", "str", "float", "bool", "list", "dict"],
    },
    {
        "id": 2,
        "round": "Round 1: Variables & Types",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What is the difference between `is` and `==`?",
        "answer": """`==` checks VALUE equality — do these two things have the same content?
`is` checks IDENTITY — are these the exact same object in memory?

Example:
  a = [1, 2, 3]
  b = [1, 2, 3]
  a == b   # True  (same values)
  a is b   # False (different objects in memory)

  c = a
  a is c   # True  (c points to the same object as a)

Common gotcha: Python caches small integers (-5 to 256) and short strings,
so `a = 5; b = 5; a is b` returns True, but don't rely on this.

INTERVIEW TIP: Always use == for comparing values. Use `is` only for
None checks: `if x is None:`""",
        "short": ["value", "identity", "memory", "object"],
    },
    {
        "id": 3,
        "round": "Round 1: Variables & Types",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What does `type()` do? What about `isinstance()`? Which is preferred?",
        "answer": """`type(x)` returns the exact type of x:
  type(42)       -> <class 'int'>
  type("hello")  -> <class 'str'>

`isinstance(x, SomeType)` checks if x is that type OR a subclass:
  isinstance(42, int)     -> True
  isinstance(True, int)   -> True  (bool is a subclass of int!)

`isinstance()` is PREFERRED because it respects inheritance.
If you have a class Dog(Animal), isinstance(dog, Animal) is True,
but type(dog) == Animal is False.

INTERVIEW TIP: Say "I'd use isinstance() because it handles
inheritance properly." That shows you understand OOP.""",
        "short": ["isinstance", "inheritance", "subclass"],
    },
    {
        "id": 4,
        "round": "Round 1: Variables & Types",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What is the difference between mutable and immutable types? Give examples.",
        "answer": """MUTABLE = can be changed after creation.
  list, dict, set — you can add/remove/modify elements.
  my_list = [1, 2, 3]
  my_list[0] = 99  # Works! List is now [99, 2, 3]

IMMUTABLE = cannot be changed after creation.
  int, float, str, tuple, frozenset, bool
  my_str = "hello"
  my_str[0] = "H"  # ERROR! Strings are immutable.
  my_str = "Hello"  # This works, but it creates a NEW string.

WHY IT MATTERS:
  1. Mutable objects can cause bugs when shared (aliasing).
  2. Only immutable objects can be dict keys or set members.
  3. Default function arguments should NOT be mutable (common gotcha).

INTERVIEW TIP: This question is almost guaranteed in junior interviews.
Know the examples cold.""",
        "short": ["mutable", "immutable", "list", "tuple", "changed"],
    },
    {
        "id": 5,
        "round": "Round 1: Variables & Types",
        "difficulty": "Easy",
        "type": "Conceptual",
        "question": "What are f-strings? How are they different from .format() and %?",
        "answer": """f-strings (formatted string literals, Python 3.6+) let you embed
expressions directly inside strings with {curly braces}:

  name = "Chint"
  age = 25
  f"Hello, {name}! You are {age} years old."

Older methods:
  "Hello, {}! You are {} years old.".format(name, age)   # .format()
  "Hello, %s! You are %d years old." % (name, age)        # % formatting

f-strings are PREFERRED because:
  1. More readable — the variable is right there in the string
  2. Faster — evaluated at runtime, no method call overhead
  3. Support expressions: f"{2 + 2}" -> "4"
  4. Support formatting: f"{3.14159:.2f}" -> "3.14"

INTERVIEW TIP: Use f-strings in all your code examples. It shows
you write modern Python.""",
        "short": ["f-string", "format", "expression", "readable"],
    },

    # =========================================================================
    # ROUND 2: DATA STRUCTURES (Easy-Medium)
    # =========================================================================

    {
        "id": 6,
        "round": "Round 2: Data Structures",
        "difficulty": "Easy-Medium",
        "type": "Conceptual",
        "question": "List vs Tuple — when would you use each?",
        "answer": """LIST — mutable, ordered, use square brackets [].
  Use when: you need to add/remove/change items.
  shopping = ["milk", "eggs", "bread"]
  shopping.append("butter")  # Can modify

TUPLE — immutable, ordered, use parentheses ().
  Use when: data should NOT change, or you need a dict key.
  coordinates = (40.7128, -74.0060)   # Lat/long shouldn't change
  rgb_color = (255, 0, 0)             # Red — fixed values

KEY DIFFERENCES:
  1. Tuples are immutable (can't modify after creation)
  2. Tuples can be dict keys; lists cannot
  3. Tuples are slightly faster and use less memory
  4. Tuples signal INTENT — "this data is fixed"

INTERVIEW TIP: Say "I use tuples for fixed collections like coordinates
or database rows, and lists when I need to modify the collection." """,
        "short": ["mutable", "immutable", "change", "key", "fixed"],
    },
    {
        "id": 7,
        "round": "Round 2: Data Structures",
        "difficulty": "Easy-Medium",
        "type": "Conceptual",
        "question": "What is a dictionary? How do you handle a missing key?",
        "answer": """A dict is a key-value mapping. Keys must be immutable (str, int, tuple).
Lookup is O(1) average — very fast regardless of size.

  user = {"name": "Chint", "age": 25}
  user["name"]   # "Chint"
  user["email"]  # KeyError!

HANDLING MISSING KEYS (3 ways):

  1. .get() — returns a default instead of crashing:
     user.get("email", "N/A")   # Returns "N/A"

  2. `in` check:
     if "email" in user:
         print(user["email"])

  3. .setdefault() — get the value OR set a default:
     user.setdefault("email", "unknown")
     # If "email" missing, sets it to "unknown" AND returns it

  4. defaultdict (from collections):
     from collections import defaultdict
     dd = defaultdict(list)
     dd["fruits"].append("apple")  # No KeyError, auto-creates []

INTERVIEW TIP: Mention .get() first — it's the most Pythonic and common.""",
        "short": ["get", "key", "value", "default", "KeyError"],
    },
    {
        "id": 8,
        "round": "Round 2: Data Structures",
        "difficulty": "Easy-Medium",
        "type": "Conceptual",
        "question": "What is a set? When would you use one?",
        "answer": """A set is an UNORDERED collection of UNIQUE elements.
No duplicates allowed, and no guaranteed order.

  numbers = {1, 2, 3, 2, 1}  # -> {1, 2, 3} (duplicates removed)

USE CASES:
  1. Remove duplicates: list(set([1, 1, 2, 3, 3])) -> [1, 2, 3]
  2. Fast membership testing: `if x in my_set` is O(1), vs O(n) for lists
  3. Set operations: union |, intersection &, difference -

  a = {1, 2, 3}
  b = {2, 3, 4}
  a | b   # {1, 2, 3, 4}  union
  a & b   # {2, 3}         intersection
  a - b   # {1}            difference

CANNOT CONTAIN: mutable types (no lists, no dicts, no other sets).
CAN CONTAIN: int, float, str, tuple, frozenset.

INTERVIEW TIP: "I'd use a set when I need unique values or fast
O(1) membership checks." Shows you understand time complexity.""",
        "short": ["unique", "unordered", "duplicate", "O(1)", "membership"],
    },
    {
        "id": 9,
        "round": "Round 2: Data Structures",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is a list comprehension? Can you also use them for dicts and sets?",
        "answer": """A list comprehension builds a new list by transforming/filtering items
in a single, readable line:

  # Traditional:
  squares = []
  for x in range(5):
      squares.append(x ** 2)

  # Comprehension:
  squares = [x ** 2 for x in range(5)]   # [0, 1, 4, 9, 16]

  # With filter:
  evens = [x for x in range(10) if x % 2 == 0]   # [0, 2, 4, 6, 8]

DICT COMPREHENSION (curly braces + colon):
  lengths = {word: len(word) for word in ["hi", "hello", "hey"]}
  # {"hi": 2, "hello": 5, "hey": 3}

SET COMPREHENSION (curly braces, no colon):
  unique_lengths = {len(word) for word in ["hi", "hello", "hey"]}
  # {2, 3, 5}

GENERATOR EXPRESSION (parentheses — lazy, memory efficient):
  total = sum(x ** 2 for x in range(1000000))  # Doesn't build a list!

INTERVIEW TIP: Use comprehensions in your code examples — it shows
you write idiomatic Python. But don't nest them 3 levels deep.""",
        "short": ["comprehension", "list", "filter", "dict", "set"],
    },

    # =========================================================================
    # ROUND 3: CONTROL FLOW & LOOPS (Medium)
    # =========================================================================

    {
        "id": 10,
        "round": "Round 3: Control Flow",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is the difference between `for` and `while` loops? When use each?",
        "answer": """`for` loop — iterate over a KNOWN sequence (list, range, string, etc.)
  for item in [1, 2, 3]:     # You know there are 3 items
      print(item)

`while` loop — repeat UNTIL a condition becomes False
  while user_input != "quit":    # Don't know when they'll quit
      user_input = input("> ")

USE FOR when:
  - Iterating over a collection (list, dict, file lines)
  - You know the number of iterations (range(10))

USE WHILE when:
  - Waiting for user input
  - Retrying until success
  - Game loops, event loops
  - You DON'T know how many iterations

COMMON PATTERNS:
  for i, item in enumerate(my_list):   # Get index + value
  for key, value in my_dict.items():   # Iterate dict
  for a, b in zip(list1, list2):       # Parallel iteration

INTERVIEW TIP: Mention enumerate() and zip() — they're Pythonic
and interviewers love seeing them.""",
        "short": ["for", "while", "sequence", "condition", "enumerate"],
    },
    {
        "id": 11,
        "round": "Round 3: Control Flow",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What do `break`, `continue`, and `pass` do?",
        "answer": """`break` — EXITS the loop entirely. No more iterations.
  for n in range(10):
      if n == 5:
          break        # Stops at 5, prints 0-4
      print(n)

`continue` — SKIPS the rest of THIS iteration, goes to next.
  for n in range(5):
      if n == 2:
          continue     # Skips 2, prints 0, 1, 3, 4
      print(n)

`pass` — Does NOTHING. It's a placeholder.
  if condition:
      pass   # TODO: implement later
  # Useful for empty functions/classes:
  def not_yet():
      pass

FOR/ELSE (bonus — rarely asked but impressive to mention):
  for item in my_list:
      if item == target:
          break
  else:
      # This runs ONLY if the loop finished WITHOUT break
      print("Not found!")

INTERVIEW TIP: Know break and continue well. Mention for/else
only if you're feeling confident — it impresses interviewers.""",
        "short": ["break", "continue", "pass", "exit", "skip", "placeholder"],
    },
    {
        "id": 12,
        "round": "Round 3: Control Flow",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What are `any()` and `all()`? Give examples.",
        "answer": """`any(iterable)` — returns True if ANY element is truthy.
`all(iterable)` — returns True if ALL elements are truthy.

  nums = [0, 1, 2, 3]
  any(nums)   # True  (1, 2, 3 are truthy)
  all(nums)   # False (0 is falsy)

WITH GENERATOR EXPRESSIONS (very Pythonic):
  ages = [22, 18, 25, 16]
  any(a >= 21 for a in ages)    # True  (22 and 25 are >= 21)
  all(a >= 18 for a in ages)    # False (16 is not >= 18)

PRACTICAL USES:
  # Check if any file exists:
  any(os.path.exists(f) for f in file_list)

  # Check if all required fields are present:
  required = ["name", "email", "password"]
  all(field in form_data for field in required)

FALSY values: 0, 0.0, "", [], {}, set(), None, False
TRUTHY: everything else

INTERVIEW TIP: Using any()/all() with generators is considered very
Pythonic. Use it in code-writing questions when checking conditions.""",
        "short": ["any", "all", "truthy", "falsy", "True"],
    },

    # =========================================================================
    # ROUND 4: FUNCTIONS (Medium)
    # =========================================================================

    {
        "id": 13,
        "round": "Round 4: Functions",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What are *args and **kwargs? When would you use them?",
        "answer": """`*args` — collects extra POSITIONAL arguments into a TUPLE.
`**kwargs` — collects extra KEYWORD arguments into a DICT.

  def example(*args, **kwargs):
      print(args)     # (1, 2, 3)
      print(kwargs)   # {"name": "Chint", "age": 25}

  example(1, 2, 3, name="Chint", age=25)

USE CASES:
  1. Flexible functions that accept variable arguments:
     def log(*messages):
         for msg in messages:
             print(f"[LOG] {msg}")

  2. Wrapper functions / decorators:
     def my_decorator(func):
         def wrapper(*args, **kwargs):    # Accept anything
             print("Before")
             result = func(*args, **kwargs)  # Pass everything through
             print("After")
             return result
         return wrapper

  3. Passing arguments through:
     def create_user(**kwargs):
         return User(**kwargs)  # Unpack dict as keyword args

ORDER in function signature:
  def f(regular, *args, keyword_only, **kwargs)

INTERVIEW TIP: Decorators are the #1 real-world use of *args/**kwargs.
If they ask "why would you need these?" — mention decorators.""",
        "short": ["args", "kwargs", "tuple", "dict", "positional", "keyword"],
    },
    {
        "id": 14,
        "round": "Round 4: Functions",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is a lambda function? When is it appropriate to use one?",
        "answer": """A lambda is an ANONYMOUS (unnamed) one-line function:

  # Regular function:
  def double(x):
      return x * 2

  # Lambda equivalent:
  double = lambda x: x * 2

GOOD USE — as a quick callback for sorting/filtering:
  names = ["Charlie", "Alice", "Bob"]
  sorted(names, key=lambda x: len(x))        # Sort by length
  sorted(names, key=lambda x: x.lower())      # Case-insensitive sort

  numbers = [1, 2, 3, 4, 5]
  list(filter(lambda x: x > 3, numbers))      # [4, 5]
  list(map(lambda x: x ** 2, numbers))         # [1, 4, 9, 16, 25]

BAD USE — anything complex. If the lambda is hard to read, use a
regular function. PEP 8 explicitly discourages assigning lambdas
to variables (just use def instead).

  # BAD:
  process = lambda x, y: x.strip().lower() + y.strip().lower()
  # GOOD:
  def process(x, y):
      return x.strip().lower() + y.strip().lower()

INTERVIEW TIP: "I use lambdas for short, throwaway functions —
mainly as the key argument for sorted()." Clean and practical.""",
        "short": ["anonymous", "one-line", "sorted", "key", "callback"],
    },
    {
        "id": 15,
        "round": "Round 4: Functions",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is variable scope in Python? What is the LEGB rule?",
        "answer": """Scope determines WHERE a variable is accessible.

LEGB rule (Python looks up variables in this order):

  L — Local:     inside the current function
  E — Enclosing: inside an outer function (for nested functions)
  G — Global:    at the module (file) level
  B — Built-in:  Python's built-in names (print, len, etc.)

  x = "global"                # G

  def outer():
      x = "enclosing"        # E
      def inner():
          x = "local"        # L
          print(x)           # "local" (found at L)
      inner()

  # If inner() didn't have x, it would check E, then G, then B.

MODIFYING outer scope:
  `global x`   — lets you modify a global variable inside a function
  `nonlocal x` — lets you modify an enclosing variable

  count = 0
  def increment():
      global count    # Without this, you'd get UnboundLocalError
      count += 1

INTERVIEW TIP: Know LEGB and be able to explain it with an example.
Mention that using `global` is generally discouraged — pass values
as arguments and return results instead.""",
        "short": ["LEGB", "local", "enclosing", "global", "built-in", "scope"],
    },
    {
        "id": 16,
        "round": "Round 4: Functions",
        "difficulty": "Medium",
        "type": "Conceptual",
        "question": "What is a decorator? Can you write a simple one?",
        "answer": """A decorator is a function that WRAPS another function to add behavior
WITHOUT modifying the original function's code.

  from functools import wraps

  def log_calls(func):
      @wraps(func)   # Preserves original function's name/docstring
      def wrapper(*args, **kwargs):
          print(f"Calling {func.__name__}...")
          result = func(*args, **kwargs)
          print(f"{func.__name__} returned {result}")
          return result
      return wrapper

  @log_calls               # Same as: greet = log_calls(greet)
  def greet(name):
      return f"Hello, {name}!"

  greet("Chint")
  # Output:
  #   Calling greet...
  #   greet returned Hello, Chint!

REAL-WORLD USES:
  - @timer — measure execution time
  - @retry — retry on failure
  - @login_required — check authentication (Flask)
  - @cache — memoize expensive computations
  - @app.route("/") — Flask routing

INTERVIEW TIP: Know how to write a basic decorator from scratch.
Mention @wraps and explain that it preserves the original function's
metadata. This is a VERY common junior dev interview question.""",
        "short": ["wraps", "wrapper", "function", "behavior", "modify"],
    },

    # =========================================================================
    # ROUND 5: OOP (Medium-Hard)
    # =========================================================================

    {
        "id": 17,
        "round": "Round 5: OOP",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is `self` in Python? Why is it needed?",
        "answer": """`self` refers to the SPECIFIC INSTANCE of the class.
It's how an object accesses its own data and methods.

  class Dog:
      def __init__(self, name):
          self.name = name        # THIS dog's name

      def bark(self):
          print(f"{self.name} says Woof!")  # THIS dog's name

  buddy = Dog("Buddy")
  rex = Dog("Rex")
  buddy.bark()  # "Buddy says Woof!" — self is buddy
  rex.bark()    # "Rex says Woof!"   — self is rex

Under the hood, Python transforms:
  buddy.bark()  ->  Dog.bark(buddy)
  rex.bark()    ->  Dog.bark(rex)

So `self` is just the first parameter — Python passes the instance
automatically. You COULD name it anything, but `self` is the universal
convention. Breaking this convention is considered very bad practice.

WHY NEEDED: Unlike Java/C++ where `this` is implicit, Python makes it
EXPLICIT. Every method must have self as its first parameter. This is
"explicit is better than implicit" — one of Python's design principles.

INTERVIEW TIP: "self is the instance itself, passed automatically by
Python. It's how methods access instance-specific data." """,
        "short": ["instance", "object", "specific", "automatic", "reference"],
    },
    {
        "id": 18,
        "round": "Round 5: OOP",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is inheritance? What does super() do?",
        "answer": """INHERITANCE lets a class (child) reuse code from another class (parent).
The child gets ALL methods and attributes of the parent automatically.

  class Animal:
      def __init__(self, name):
          self.name = name
      def speak(self):
          print(f"{self.name} makes a sound")

  class Dog(Animal):              # Dog inherits from Animal
      def __init__(self, name, breed):
          super().__init__(name)  # Call Animal's __init__
          self.breed = breed      # Add dog-specific data
      def fetch(self):
          print(f"{self.name} fetches!")  # Dog-only method

  d = Dog("Buddy", "Lab")
  d.speak()   # Inherited from Animal
  d.fetch()   # Dog's own method

`super()` calls the PARENT class's method. Most commonly used in
__init__ to initialize the parent's attributes before adding your own.

METHOD RESOLUTION ORDER (MRO):
  Python uses C3 linearization to determine which parent's method to
  call when there's multiple inheritance. Check with: Dog.__mro__

INTERVIEW TIP: Keep your inheritance example simple (Animal -> Dog).
Mention super().__init__() — forgetting it is a common bug.""",
        "short": ["parent", "child", "super", "reuse", "inherit"],
    },
    {
        "id": 19,
        "round": "Round 5: OOP",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What are dunder methods? Name the most important ones.",
        "answer": """Dunder (double-under) methods are special methods with __name__ format.
Python calls them automatically in specific situations.

MOST IMPORTANT:
  __init__(self, ...)        Constructor — called when creating an object
  __str__(self)              Called by print() and str() — human-readable
  __repr__(self)             Called by repr() — unambiguous, for debugging
  __eq__(self, other)        Called by == operator
  __len__(self)              Called by len()
  __getitem__(self, key)     Called by obj[key]
  __iter__(self)             Makes object iterable (for loops)
  __contains__(self, item)   Called by `in` operator

OPERATORS:
  __add__(self, other)       obj1 + obj2
  __lt__(self, other)        obj1 < obj2
  __bool__(self)             Called by bool() and if statements

EXAMPLE:
  class Playlist:
      def __init__(self, name, songs):
          self.name = name
          self.songs = songs
      def __len__(self):
          return len(self.songs)
      def __str__(self):
          return f"Playlist({self.name}, {len(self)} songs)"
      def __contains__(self, song):
          return song in self.songs

  p = Playlist("Chill", ["Song A", "Song B"])
  print(len(p))           # 2        (__len__)
  print(p)                # Playlist(Chill, 2 songs)  (__str__)
  print("Song A" in p)    # True     (__contains__)

INTERVIEW TIP: Know __init__, __str__, __repr__, __eq__, __len__.
Being able to implement __str__ and __repr__ is a common ask.""",
        "short": ["__init__", "__str__", "__repr__", "special", "magic"],
    },
    {
        "id": 20,
        "round": "Round 5: OOP",
        "difficulty": "Medium-Hard",
        "type": "Conceptual",
        "question": "What is the difference between a class method, static method, and instance method?",
        "answer": """INSTANCE METHOD (most common):
  - Takes `self` as first argument
  - Can access and modify instance AND class state
  def greet(self):
      return f"Hello, {self.name}"

CLASS METHOD (@classmethod):
  - Takes `cls` (the class itself) as first argument
  - Can modify class state, but NOT instance state
  - Often used as alternative constructors

  @classmethod
  def from_string(cls, data_string):
      name, age = data_string.split("-")
      return cls(name, int(age))   # Creates a new instance

  user = User.from_string("Chint-25")  # Alternative constructor

STATIC METHOD (@staticmethod):
  - Takes NO self or cls — just a regular function
  - Doesn't access instance or class state
  - Belongs to the class for organizational purposes

  @staticmethod
  def is_valid_age(age):
      return 0 < age < 150

WHEN TO USE:
  - Instance method: 95% of the time (needs self)
  - Class method: alternative constructors, factory methods
  - Static method: utility functions that logically belong to the class

INTERVIEW TIP: The classic follow-up is "give an example of @classmethod."
Always say "alternative constructor" — it's the textbook answer.""",
        "short": ["self", "cls", "classmethod", "staticmethod", "instance"],
    },

    # =========================================================================
    # ROUND 6: COMMON GOTCHAS & TRICKY BEHAVIOR (Hard)
    # =========================================================================

    {
        "id": 21,
        "round": "Round 6: Gotchas",
        "difficulty": "Hard",
        "type": "Conceptual",
        "question": "What is the mutable default argument bug? How do you fix it?",
        "answer": """THE BUG:
  def add_item(item, items=[]):    # DEFAULT LIST IS SHARED!
      items.append(item)
      return items

  print(add_item("a"))   # ["a"]       — looks fine
  print(add_item("b"))   # ["a", "b"]  — WAIT WHAT?!

The default [] is created ONCE when the function is defined, not each
time it's called. So every call shares the SAME list object.

THE FIX — use None as default, create a new list inside:
  def add_item(item, items=None):
      if items is None:
          items = []    # New list for each call
      items.append(item)
      return items

  print(add_item("a"))   # ["a"]
  print(add_item("b"))   # ["b"]  — correct!

This applies to ALL mutable defaults: lists, dicts, sets.

WHY: Python evaluates default arguments at function DEFINITION time,
not at call time. Immutable defaults (int, str, None) are fine because
they can't be modified in place.

INTERVIEW TIP: This is one of the TOP Python gotchas asked in interviews.
Know the bug AND the fix (use None).""",
        "short": ["None", "mutable", "default", "shared", "definition"],
    },
    {
        "id": 22,
        "round": "Round 6: Gotchas",
        "difficulty": "Hard",
        "type": "Conceptual",
        "question": "What is the difference between shallow copy and deep copy?",
        "answer": """SHALLOW COPY — copies the outer object, but inner objects are SHARED.
  import copy
  original = [[1, 2], [3, 4]]
  shallow = copy.copy(original)    # or original.copy() or list(original)

  shallow[0][0] = 99
  print(original)   # [[99, 2], [3, 4]]  — ORIGINAL CHANGED!
  # Because shallow[0] and original[0] point to the SAME inner list.

  shallow.append([5, 6])
  print(original)   # [[99, 2], [3, 4]]  — outer is independent
  print(shallow)    # [[99, 2], [3, 4], [5, 6]]

DEEP COPY — copies EVERYTHING, recursively. Fully independent.
  deep = copy.deepcopy(original)
  deep[0][0] = 999
  print(original)   # [[99, 2], [3, 4]]  — NOT changed!

METHODS:
  list.copy() or list(x)     — shallow copy
  copy.copy(x)               — shallow copy (works on any object)
  copy.deepcopy(x)           — deep copy

WHEN TO USE DEEP COPY:
  When you have nested mutable objects (list of lists, dict of dicts)
  and need a fully independent copy.

INTERVIEW TIP: Draw it out mentally. "Shallow copy duplicates the
container but shares the contents. Deep copy duplicates everything." """,
        "short": ["shallow", "deep", "nested", "shared", "independent", "deepcopy"],
    },
    {
        "id": 23,
        "round": "Round 6: Gotchas",
        "difficulty": "Hard",
        "type": "Conceptual",
        "question": "What are generators? How are they different from regular functions?",
        "answer": """A generator is a function that uses `yield` instead of `return`.
It produces values ONE AT A TIME (lazily) instead of all at once.

  def count_up(n):
      i = 1
      while i <= n:
          yield i        # Pause here, produce i, resume later
          i += 1

  for num in count_up(3):
      print(num)         # 1, 2, 3

KEY DIFFERENCES:
  Regular function:
    - return gives back ONE value and the function is DONE
    - All data computed upfront, stored in memory

  Generator function:
    - yield produces a value and PAUSES, resumes on next()
    - Values computed on-demand (lazy evaluation)
    - Only ONE value in memory at a time

MEMORY BENEFIT:
  big_list = [x ** 2 for x in range(10_000_000)]    # ~80MB in memory
  big_gen  = (x ** 2 for x in range(10_000_000))    # ~100 bytes!

USE CASES:
  - Processing large files line by line
  - Infinite sequences (e.g., Fibonacci)
  - Pipelines of data transformations
  - Any time you don't need all results at once

INTERVIEW TIP: "Generators are memory-efficient because they compute
values lazily, one at a time." Show you understand the memory benefit.""",
        "short": ["yield", "lazy", "memory", "one at a time", "pause"],
    },

    # =========================================================================
    # ROUND 7: OUTPUT PREDICTION (Hard)
    # =========================================================================

    {
        "id": 24,
        "round": "Round 7: What Does This Print?",
        "difficulty": "Hard",
        "type": "Output",
        "question": "What does this code print?\n\n  x = [1, 2, 3]\n  y = x\n  y.append(4)\n  print(x)",
        "answer": """OUTPUT: [1, 2, 3, 4]

WHY: y = x does NOT copy the list. Both x and y point to the SAME
list object in memory. When you modify through y, x sees it too.

This is called ALIASING. It's one of the most common beginner bugs.

  x = [1, 2, 3]
  y = x           # y is an ALIAS for x, not a copy
  y.append(4)     # Modifies the shared list
  print(x)        # [1, 2, 3, 4] — x is affected!

TO ACTUALLY COPY:
  y = x.copy()    # Shallow copy
  y = x[:]        # Slice copy
  y = list(x)     # Constructor copy""",
        "short": ["[1, 2, 3, 4]"],
        "code": "x = [1, 2, 3]\ny = x\ny.append(4)\nprint(x)",
    },
    {
        "id": 25,
        "round": "Round 7: What Does This Print?",
        "difficulty": "Hard",
        "type": "Output",
        "question": "What does this code print?\n\n  def foo(a, b=[]):\n      b.append(a)\n      return b\n\n  print(foo(1))\n  print(foo(2))\n  print(foo(3))",
        "answer": """OUTPUT:
  [1]
  [1, 2]
  [1, 2, 3]

WHY: This is the mutable default argument gotcha!
The default list [] is created ONCE when the function is defined.
Every call without passing `b` shares the SAME list.

  foo(1) -> appends 1 to the shared [] -> [1]
  foo(2) -> appends 2 to the same list -> [1, 2]
  foo(3) -> appends 3 to the same list -> [1, 2, 3]

FIX:
  def foo(a, b=None):
      if b is None:
          b = []
      b.append(a)
      return b""",
        "short": ["[1]", "[1, 2]", "[1, 2, 3]"],
        "code": "def foo(a, b=[]):\n    b.append(a)\n    return b\n\nprint(foo(1))\nprint(foo(2))\nprint(foo(3))",
    },
    {
        "id": 26,
        "round": "Round 7: What Does This Print?",
        "difficulty": "Hard",
        "type": "Output",
        "question": "What does this code print?\n\n  for i in range(3):\n      pass\n  print(i)",
        "answer": """OUTPUT: 2

WHY: In Python, the loop variable `i` is NOT scoped to the loop.
It persists after the loop ends with its LAST value.

  range(3) produces 0, 1, 2
  After the loop, i still equals 2 (the last value)

This is different from languages like Java or C++ where loop
variables are scoped to the loop block.

NOTE: If the loop never executes (e.g., range(0)), then `i` is
never created, and print(i) would raise NameError.""",
        "short": ["2"],
        "code": "for i in range(3):\n    pass\nprint(i)",
    },
    {
        "id": 27,
        "round": "Round 7: What Does This Print?",
        "difficulty": "Hard",
        "type": "Output",
        "question": "What does this code print?\n\n  print(bool(\"\"), bool(\" \"), bool(0), bool([]), bool([0]))",
        "answer": """OUTPUT: False True False False True

  bool(\"\")    -> False  (empty string is falsy)
  bool(\" \")   -> True   (string with a space is NOT empty!)
  bool(0)     -> False  (zero is falsy)
  bool([])    -> False  (empty list is falsy)
  bool([0])   -> True   (list with one element is NOT empty!)

FALSY VALUES in Python:
  False, None, 0, 0.0, "", [], {}, set(), ()

EVERYTHING ELSE is truthy. The key insight:
  - " " (space) is truthy because the string is not empty
  - [0] is truthy because the list is not empty (it has one element)
  - It's the CONTAINER being empty/non-empty that matters, not the content""",
        "short": ["False", "True", "False", "False", "True"],
        "code": 'print(bool(""), bool(" "), bool(0), bool([]), bool([0]))',
    },

    # =========================================================================
    # ROUND 8: BUG FIXING & CODE WRITING (Practical)
    # =========================================================================

    {
        "id": 28,
        "round": "Round 8: Practical",
        "difficulty": "Medium",
        "type": "Bug Fix",
        "question": "What is wrong with this code? How would you fix it?\n\n  def get_even_numbers(numbers):\n      evens = []\n      for num in numbers:\n          if num % 2 = 0:\n              evens.append(num)\n      return evens",
        "answer": """BUG: `num % 2 = 0` uses a single `=` (assignment) instead of `==` (comparison).

  if num % 2 = 0:    # WRONG — = is assignment
  if num % 2 == 0:   # RIGHT — == is comparison

FIXED CODE:
  def get_even_numbers(numbers):
      evens = []
      for num in numbers:
          if num % 2 == 0:    # Fixed: == not =
              evens.append(num)
      return evens

EVEN BETTER (Pythonic):
  def get_even_numbers(numbers):
      return [num for num in numbers if num % 2 == 0]

This is a trick question — it's a syntax error that Python would
catch immediately. But it tests whether you read code carefully.""",
        "short": ["==", "comparison", "assignment", "equals"],
        "code": "def get_even_numbers(numbers):\n    evens = []\n    for num in numbers:\n        if num % 2 = 0:\n            evens.append(num)\n    return evens",
    },
    {
        "id": 29,
        "round": "Round 8: Practical",
        "difficulty": "Medium",
        "type": "Code Writing",
        "question": "Write a function that takes a list of numbers and returns a dict with\n'min', 'max', 'avg', and 'count' keys. Handle the empty list case.",
        "answer": """SOLUTION:
  def stats(numbers):
      if not numbers:
          return {"min": None, "max": None, "avg": None, "count": 0}
      return {
          "min": min(numbers),
          "max": max(numbers),
          "avg": sum(numbers) / len(numbers),
          "count": len(numbers),
      }

  # Test:
  print(stats([1, 2, 3, 4, 5]))
  # {"min": 1, "max": 5, "avg": 3.0, "count": 5}

  print(stats([]))
  # {"min": None, "max": None, "avg": None, "count": 0}

KEY POINTS:
  1. Handle edge case (empty list) FIRST — shows defensive programming
  2. Use built-in functions (min, max, sum, len) — don't reinvent
  3. Return a dict for structured data — clean and readable
  4. avg uses / (true division), not // (floor division)

INTERVIEW TIP: Always handle edge cases first. Ask "what should
happen if the list is empty?" before writing code. That impresses.""",
        "short": ["min", "max", "sum", "len", "empty", "None"],
    },
    {
        "id": 30,
        "round": "Round 8: Practical",
        "difficulty": "Hard",
        "type": "Code Writing",
        "question": "Write a function `flatten(nested_list)` that flattens a nested list\nof any depth. Example: flatten([1, [2, [3, 4], 5], 6]) -> [1, 2, 3, 4, 5, 6]",
        "answer": """SOLUTION (recursive):
  def flatten(nested_list):
      result = []
      for item in nested_list:
          if isinstance(item, list):
              result.extend(flatten(item))   # Recurse into sublists
          else:
              result.append(item)
      return result

  print(flatten([1, [2, [3, 4], 5], 6]))
  # [1, 2, 3, 4, 5, 6]

HOW IT WORKS:
  flatten([1, [2, [3, 4], 5], 6])
    1 -> not a list -> append 1
    [2, [3, 4], 5] -> is a list -> recurse:
      flatten([2, [3, 4], 5])
        2 -> append 2
        [3, 4] -> recurse:
          flatten([3, 4])
            3 -> append 3
            4 -> append 4
            return [3, 4]
        5 -> append 5
        return [2, 3, 4, 5]
    6 -> append 6
  return [1, 2, 3, 4, 5, 6]

ALTERNATIVE (generator):
  def flatten(lst):
      for item in lst:
          if isinstance(item, list):
              yield from flatten(item)
          else:
              yield item

INTERVIEW TIP: Start with the recursive approach — it's clearest.
If they ask for optimization, mention the generator version with
yield from. Always ask about expected depth to discuss recursion limits.""",
        "short": ["recursive", "isinstance", "list", "extend", "append"],
    },
]


# =============================================================================
#  STUDY GUIDE MODE — Print all questions with detailed answers
# =============================================================================

def print_study_guide():
    """Print all questions with full answers for studying."""
    print()
    print("=" * 70)
    print("  PYTHON INTERVIEW STUDY GUIDE — JUNIOR DEV / INTERN LEVEL")
    print("  30 Questions with Detailed Answers")
    print("=" * 70)

    current_round = ""
    for q in QUESTIONS:
        # Print round header when it changes
        if q["round"] != current_round:
            current_round = q["round"]
            print()
            print()
            print("=" * 70)
            print(f"  {current_round}")
            print("=" * 70)

        print()
        print(f"  Q{q['id']}. [{q['difficulty']}] [{q['type']}]")
        print(f"  {'-' * 60}")

        # Print question
        for line in q["question"].split("\n"):
            print(f"  {line}")

        # Print code block if exists
        if q.get("code"):
            print()
            print("  Code:")
            for line in q["code"].split("\n"):
                print(f"    {line}")

        # Print answer
        print()
        print("  ANSWER:")
        for line in q["answer"].split("\n"):
            print(f"  {line}")

        print()
        print(f"  {'~' * 60}")

    print()
    print("=" * 70)
    print("  END OF STUDY GUIDE")
    print("=" * 70)
    print()
    print("  TIPS FOR YOUR INTERVIEW:")
    print("  1. Practice explaining these out loud — not just reading.")
    print("  2. For code questions, write the code by hand (no IDE).")
    print("  3. Always ask clarifying questions before coding.")
    print("  4. Handle edge cases first — it shows maturity.")
    print("  5. If stuck, talk through your thought process.")
    print("  6. Use Python idioms (f-strings, comprehensions, enumerate).")
    print()


# =============================================================================
#  INTERACTIVE QUIZ MODE
# =============================================================================

def run_quiz():
    """Run the interactive quiz in the terminal."""
    print()
    print("=" * 70)
    print("  PYTHON INTERVIEW QUIZ — JUNIOR DEV / INTERN LEVEL")
    print("  30 Questions | Type your answer, then see the full explanation")
    print("=" * 70)
    print()
    print("  HOW IT WORKS:")
    print("  - Each question will be shown one at a time")
    print("  - Type your answer (doesn't need to be perfect)")
    print("  - Press Enter to submit")
    print("  - You'll see the full answer + whether you got key points")
    print("  - Type 'skip' to skip, 'quit' to exit early")
    print()
    input("  Press Enter to start... ")

    score = 0
    answered = 0
    skipped = 0
    results = []
    current_round = ""

    for q in QUESTIONS:
        # Print round header when it changes
        if q["round"] != current_round:
            current_round = q["round"]
            print()
            print("=" * 70)
            print(f"  {current_round}")
            print("=" * 70)

        print()
        print(f"  Q{q['id']}/{len(QUESTIONS)} [{q['difficulty']}] [{q['type']}]")
        print(f"  {'-' * 60}")

        # Print question
        for line in q["question"].split("\n"):
            print(f"  {line}")

        # Print code block if exists
        if q.get("code"):
            print()
            print("  Code:")
            for line in q["code"].split("\n"):
                print(f"    {line}")

        print()

        # Get user's answer
        try:
            user_answer = input("  Your answer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Quiz ended early.")
            break

        if user_answer.lower() == "quit":
            print("\n  Quiz ended early.")
            break

        if user_answer.lower() == "skip":
            skipped += 1
            results.append({"id": q["id"], "status": "skipped"})
            print("  Skipped!")
            # Still show the answer
            print()
            print("  ANSWER:")
            for line in q["answer"].split("\n"):
                print(f"  {line}")
            input("\n  Press Enter for next question... ")
            continue

        answered += 1

        # Check if they hit key points
        user_lower = user_answer.lower()
        hits = [kw for kw in q["short"] if kw.lower() in user_lower]
        hit_ratio = len(hits) / len(q["short"]) if q["short"] else 0

        if hit_ratio >= 0.4:
            score += 1
            status = "GOOD"
            verdict = "You hit the key points!"
        elif hit_ratio > 0:
            score += 0.5
            status = "PARTIAL"
            verdict = "You got some of it — read the full answer:"
        else:
            status = "MISS"
            verdict = "Review this one — here's the full answer:"

        results.append({
            "id": q["id"],
            "status": status,
            "hits": hits,
            "total_keywords": len(q["short"]),
        })

        print()
        if status == "GOOD":
            print(f"  >> {verdict}")
        else:
            print(f"  >> {verdict}")

        print()
        print("  FULL ANSWER:")
        for line in q["answer"].split("\n"):
            print(f"  {line}")

        try:
            input("\n  Press Enter for next question... ")
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Quiz ended early.")
            break

    # =========================================================================
    # SCORE SUMMARY
    # =========================================================================
    print()
    print("=" * 70)
    print("  QUIZ RESULTS")
    print("=" * 70)
    print()

    total_possible = answered
    percentage = (score / total_possible * 100) if total_possible > 0 else 0

    print(f"  Score: {score}/{total_possible} ({percentage:.0f}%)")
    print(f"  Answered: {answered}")
    print(f"  Skipped: {skipped}")
    print()

    # Rating
    if percentage >= 85:
        rating = "EXCELLENT"
        msg = "You're well-prepared for a junior dev interview!"
    elif percentage >= 70:
        rating = "GOOD"
        msg = "Solid foundation. Review the ones you missed."
    elif percentage >= 50:
        rating = "DECENT"
        msg = "You know the basics but need to study more."
    elif percentage >= 30:
        rating = "NEEDS WORK"
        msg = "Go through the study guide (python interview_python_basics.py study)"
    else:
        rating = "KEEP STUDYING"
        msg = "Review the python_course chapters, then try again!"

    print(f"  Rating: {rating}")
    print(f"  {msg}")
    print()

    # Show what to review
    missed = [r for r in results if r["status"] in ("MISS", "PARTIAL")]
    if missed:
        print("  REVIEW THESE QUESTIONS:")
        for r in missed:
            q_data = QUESTIONS[r["id"] - 1]
            marker = "~" if r["status"] == "PARTIAL" else "X"
            print(f"    [{marker}] Q{r['id']}: {q_data['question'].split(chr(10))[0][:55]}...")
        print()
        print("  Run with 'study' to see all answers:")
        print("    python interview_python_basics.py study")
    else:
        print("  You nailed everything! Try explaining these to someone else —")
        print("  teaching is the best way to solidify knowledge.")

    print()
    print("=" * 70)
    print()


# =============================================================================
#  MAIN — Choose mode based on command line args
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "study":
        print_study_guide()
    elif len(sys.argv) > 1 and sys.argv[1].lower() == "help":
        print()
        print("  Usage:")
        print("    python interview_python_basics.py          Interactive quiz")
        print("    python interview_python_basics.py study    Print study guide")
        print("    python interview_python_basics.py help     Show this help")
        print()
    else:
        run_quiz()
