"""
=====================================================
 CHAPTER 6: FILE I/O & EXCEPTION HANDLING
=====================================================

Programs need to:
  - READ files (config files, data files, user uploads)
  - WRITE files (logs, exports, generated content)
  - HANDLE ERRORS gracefully (don't crash, tell the user what went wrong)


HOW TO RUN:
  python ch6_file_io_and_exceptions.py
"""

import os
import json

# =============================================================================
# PART 1: READING FILES
# =============================================================================

print("=" * 40)
print("PART 1: Reading files")
print("=" * 40)

# First, create a sample file to work with:
with open("sample.txt", "w") as f:
    f.write("Line 1: Hello World\n")
    f.write("Line 2: Python is great\n")
    f.write("Line 3: File I/O is easy\n")

# The WITH statement (context manager):
# - Opens the file
# - Gives you the file object as 'f'
# - AUTOMATICALLY closes the file when the block ends
# - Even if an error occurs!

# Read entire file as one string:
with open("sample.txt", "r") as f:
    content = f.read()
print(f"Full content:\n{content}")

# Read as a list of lines:
with open("sample.txt", "r") as f:
    lines = f.readlines()
print(f"Lines: {lines}")  # Each line includes \n

# Read line by line (memory efficient for big files):
print("Line by line:")
with open("sample.txt", "r") as f:
    for line in f:
        print(f"  {line.strip()}")  # strip() removes \n
print()


# =============================================================================
# PART 2: WRITING FILES
# =============================================================================

print("=" * 40)
print("PART 2: Writing files")
print("=" * 40)

# "w" = write (creates file, OVERWRITES if exists)
with open("output.txt", "w") as f:
    f.write("This is line 1\n")
    f.write("This is line 2\n")
print("Wrote output.txt")

# "a" = append (adds to end of file, creates if doesn't exist)
with open("output.txt", "a") as f:
    f.write("This is line 3 (appended)\n")
print("Appended to output.txt")

# Write a list of lines:
lines = ["First\n", "Second\n", "Third\n"]
with open("output.txt", "w") as f:
    f.writelines(lines)
print("Wrote lines to output.txt")

# Read it back to verify:
with open("output.txt", "r") as f:
    print(f"Content: {f.read()}")


# =============================================================================
# PART 3: WORKING WITH JSON
# =============================================================================
#
# JSON is THE standard format for data exchange.
# Python dicts/lists map directly to JSON.

print("=" * 40)
print("PART 3: JSON files")
print("=" * 40)

# Python dict -> JSON file
data = {
    "name": "Chint",
    "age": 25,
    "languages": ["Python", "JavaScript"],
    "is_student": True,
}

# Write JSON:
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)  # indent=2 for pretty formatting
print("Wrote data.json")

# Read JSON:
with open("data.json", "r") as f:
    loaded = json.load(f)
print(f"Loaded: {loaded}")
print(f"Name: {loaded['name']}")
print()

# JSON string (not file):
json_string = json.dumps(data, indent=2)  # dict -> JSON string
print(f"JSON string:\n{json_string}")

parsed = json.loads(json_string)  # JSON string -> dict
print(f"Parsed back: {parsed['name']}")
print()


# =============================================================================
# PART 4: EXCEPTION HANDLING (TRY / EXCEPT)
# =============================================================================
#
# Errors happen. Files don't exist, users enter bad data, APIs are down.
# try/except lets you handle errors GRACEFULLY instead of crashing.

print("=" * 40)
print("PART 4: Exception handling")
print("=" * 40)

# Without try/except:
#   result = 10 / 0  # CRASH! ZeroDivisionError

# With try/except:
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero!")

# Catching specific exceptions:
try:
    number = int("not_a_number")
except ValueError as e:
    print(f"ValueError: {e}")

# Catching file errors:
try:
    with open("nonexistent.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File doesn't exist!")

# Multiple except blocks:
try:
    data = {"a": 1}
    value = data["b"]  # KeyError
except KeyError:
    print("Key not found in dict!")
except Exception as e:
    print(f"Some other error: {e}")
print()


# try / except / else / finally:
print("Full try/except structure:")
try:
    result = 10 / 2
except ZeroDivisionError:
    print("  Division error!")
else:
    # Runs ONLY if no exception occurred
    print(f"  Success! Result: {result}")
finally:
    # ALWAYS runs, exception or not (cleanup)
    print("  Finally block (always runs)")
print()


# =============================================================================
# PART 5: RAISING EXCEPTIONS
# =============================================================================
#
# You can RAISE your own exceptions to signal errors.

print("=" * 40)
print("PART 5: Raising exceptions")
print("=" * 40)


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Caught: {e}")

# Custom exception classes:
class InsufficientFundsError(Exception):
    """Custom exception for bank withdrawals."""
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(f"Need ${amount} but only have ${balance}")
    return balance - amount

try:
    new_balance = withdraw(100, 200)
except InsufficientFundsError as e:
    print(f"Bank error: {e}")
print()


# =============================================================================
# PART 6: COMMON EXCEPTIONS REFERENCE
# =============================================================================
#
# ValueError:      Wrong value type     int("abc")
# TypeError:       Wrong type           "2" + 2
# KeyError:        Missing dict key     d["missing"]
# IndexError:      List index out       [1,2][5]
# FileNotFoundError: File doesn't exist open("nope.txt")
# ZeroDivisionError: Divide by zero     1 / 0
# AttributeError:  Missing attribute    "str".foo()
# ImportError:      Can't import        import nonexistent
# NameError:        Undefined variable  print(undefined_var)


# CLEANUP
os.remove("sample.txt")
os.remove("output.txt")
os.remove("data.json")
print("Cleaned up temp files.")


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Read:   with open("f.txt", "r") as f: content = f.read()
# Write:  with open("f.txt", "w") as f: f.write("text")
# Append: with open("f.txt", "a") as f: f.write("more")
# JSON:   json.dump(obj, file) / json.load(file)
#         json.dumps(obj) / json.loads(string)
#
# try:
#     risky_code()
# except SpecificError as e:
#     handle_error()
# else:
#     success()
# finally:
#     always_runs()
#
# raise ValueError("message")
#
# =============================================================================
