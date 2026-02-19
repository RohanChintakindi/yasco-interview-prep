"""
=====================================================
 CHAPTER 1: VARIABLES, TYPES & PRINT
=====================================================

WHAT IS PYTHON?
---------------
Python is a programming language. A programming language lets you
give instructions to a computer in a way it can understand.

Python is special because:
  - Readable: code looks almost like English
  - Beginner-friendly: less boilerplate than Java/C++
  - Powerful: used by Google, Netflix, NASA, Instagram
  - Versatile: web apps, AI, data science, automation, games


HOW TO RUN:
  python ch1_variables_and_types.py
"""

# =============================================================================
# PART 1: PRINT - SHOWING OUTPUT
# =============================================================================
#
# print() displays text in the terminal.
# It's how you see what your program is doing.

print("Hello, World!")  # Your first Python line!
print("Python is awesome")
print(42)               # Can print numbers too
print(3.14)             # And decimals
print()                 # Empty line


# =============================================================================
# PART 2: VARIABLES - STORING DATA
# =============================================================================
#
# A variable is a NAME that holds a VALUE.
# Think of it like a labeled box:
#   name = "Chint"   -> box labeled "name" contains "Chint"
#   age = 25         -> box labeled "age" contains 25
#
# You CREATE a variable by assigning a value with =

print("=" * 40)
print("PART 2: Variables")
print("=" * 40)

name = "Chint"
age = 25
height = 5.9
is_student = True

print(name)        # Chint
print(age)         # 25
print(height)      # 5.9
print(is_student)  # True
print()

# Variables can be REASSIGNED (the box gets a new value):
age = 26           # age was 25, now it's 26
print(f"Happy birthday! Now {age}")
print()

# NAMING RULES:
#   - Must start with a letter or underscore: name, _name, name2
#   - Can't start with a number: 2name (WRONG)
#   - No spaces: my name (WRONG), use my_name (RIGHT)
#   - Case sensitive: Name and name are DIFFERENT variables
#   - Convention: use snake_case (words_separated_by_underscores)


# =============================================================================
# PART 3: DATA TYPES
# =============================================================================
#
# Every value in Python has a TYPE. The type determines what you can do with it.
#
# TYPE       | EXAMPLE          | WHAT IT IS
# -----------+------------------+---------------------------------
# str        | "hello"          | Text (string of characters)
# int        | 42               | Whole number (integer)
# float      | 3.14             | Decimal number
# bool       | True / False     | Yes/No value (boolean)
# NoneType   | None             | "Nothing" / "No value"

print("=" * 40)
print("PART 3: Data Types")
print("=" * 40)

text = "Hello"         # str
whole_number = 42      # int
decimal = 3.14         # float
yes_no = True          # bool
nothing = None         # NoneType

# type() tells you what type a value is:
print(f"'{text}' is {type(text)}")
print(f"{whole_number} is {type(whole_number)}")
print(f"{decimal} is {type(decimal)}")
print(f"{yes_no} is {type(yes_no)}")
print(f"{nothing} is {type(nothing)}")
print()


# =============================================================================
# PART 4: STRINGS (TEXT)
# =============================================================================
#
# Strings are text. Wrap them in quotes (single or double, both work).

print("=" * 40)
print("PART 4: Strings")
print("=" * 40)

greeting = "Hello"
name = 'Chint'       # Single quotes work too

# CONCATENATION (joining strings):
full = greeting + ", " + name + "!"
print(full)  # Hello, Chint!

# F-STRINGS (the modern way - much better):
# Put f before the quote, then use {variable} inside
message = f"Hello, {name}! You are {age} years old."
print(message)

# You can put ANY expression inside {}:
print(f"2 + 2 = {2 + 2}")
print(f"Name in uppercase: {name.upper()}")
print(f"Name length: {len(name)} characters")
print()

# STRING METHODS (useful operations):
text = "  Hello, World!  "
print(f"Original:  '{text}'")
print(f"Strip:     '{text.strip()}'")      # Remove whitespace
print(f"Lower:     '{text.strip().lower()}'")
print(f"Upper:     '{text.strip().upper()}'")
print(f"Replace:   '{text.strip().replace('World', 'Python')}'")
print(f"Split:     {text.strip().split(', ')}")  # Split into list
print(f"Starts with 'He': {text.strip().startswith('He')}")
print()


# =============================================================================
# PART 5: NUMBERS & MATH
# =============================================================================

print("=" * 40)
print("PART 5: Numbers & Math")
print("=" * 40)

a = 10
b = 3

print(f"{a} + {b} = {a + b}")       # Addition: 13
print(f"{a} - {b} = {a - b}")       # Subtraction: 7
print(f"{a} * {b} = {a * b}")       # Multiplication: 30
print(f"{a} / {b} = {a / b}")       # Division: 3.333... (always float)
print(f"{a} // {b} = {a // b}")     # Floor division: 3 (no decimal)
print(f"{a} % {b} = {a % b}")       # Modulo (remainder): 1
print(f"{a} ** {b} = {a ** b}")     # Exponent: 1000 (10^3)
print()

# TYPE CONVERSION:
num_str = "42"
num = int(num_str)     # str -> int
print(f"String '42' + 8 = {num + 8}")  # 50

pi_str = "3.14"
pi = float(pi_str)     # str -> float
print(f"Pi = {pi}")

back_to_str = str(42)  # int -> str
print(f"Type: {type(back_to_str)}")  # <class 'str'>
print()


# =============================================================================
# PART 6: BOOLEANS & COMPARISONS
# =============================================================================

print("=" * 40)
print("PART 6: Booleans & Comparisons")
print("=" * 40)

# Booleans are True or False (capitalized!)
is_raining = False
is_sunny = True
print(f"Raining: {is_raining}, Sunny: {is_sunny}")

# Comparison operators (return True or False):
x = 10
print(f"{x} == 10: {x == 10}")   # Equal to
print(f"{x} != 5:  {x != 5}")    # Not equal to
print(f"{x} > 5:   {x > 5}")     # Greater than
print(f"{x} < 20:  {x < 20}")    # Less than
print(f"{x} >= 10: {x >= 10}")   # Greater or equal
print(f"{x} <= 9:  {x <= 9}")    # Less or equal

# Logical operators:
print(f"True and False: {True and False}")  # Both must be True -> False
print(f"True or False:  {True or False}")   # At least one True -> True
print(f"not True:       {not True}")        # Opposite -> False
print()


# =============================================================================
# PART 7: INPUT - GETTING DATA FROM THE USER
# =============================================================================
#
# input() pauses and waits for the user to type something.
# It ALWAYS returns a string (even if they type a number).

print("=" * 40)
print("PART 7: User Input")
print("=" * 40)

# Uncomment these lines to try interactive input:
# user_name = input("What's your name? ")
# user_age = input("How old are you? ")
# print(f"Hello {user_name}! You'll be {int(user_age) + 1} next year.")

# Note: input() returns a STRING. To do math, convert with int() or float():
# age = int(input("Age: "))  # Now age is an integer

print("(Uncomment the input lines in the code to try this interactively)")
print()


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Print:       print("text"), print(variable), print(f"text {var}")
# Variables:   name = value
# Types:       str, int, float, bool, None
# F-strings:   f"Hello {name}, you are {age}"
# Math:        +  -  *  /  //  %  **
# Compare:     ==  !=  >  <  >=  <=
# Logic:       and  or  not
# Convert:     int("42")  float("3.14")  str(42)
# Type check:  type(variable)
# Input:       name = input("Prompt: ")
#
# =============================================================================
