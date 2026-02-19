"""
=====================================================
 CHAPTER 8: MODULES, PACKAGES & VIRTUAL ENVIRONMENTS
=====================================================

As your code grows, you split it into MODULES (separate .py files)
and use PACKAGES (libraries other people wrote).

This chapter covers:
  - Importing modules
  - Creating your own modules
  - pip (installing packages)
  - Virtual environments
  - The Python standard library


HOW TO RUN:
  python ch8_modules_and_packages.py
"""

# =============================================================================
# PART 1: IMPORTING MODULES
# =============================================================================
#
# A module is just a .py file. Importing it lets you use its code.

print("=" * 40)
print("PART 1: Importing")
print("=" * 40)

# Import the entire module:
import math
print(f"pi = {math.pi}")
print(f"sqrt(16) = {math.sqrt(16)}")

# Import specific things:
from datetime import datetime, timedelta
now = datetime.now()
print(f"Now: {now.strftime('%Y-%m-%d %H:%M')}")
print(f"Tomorrow: {(now + timedelta(days=1)).strftime('%Y-%m-%d')}")

# Import with alias:
import json as j
data = j.dumps({"name": "Chint"})
print(f"JSON: {data}")

# Import everything (avoid this - pollutes namespace):
# from math import *

print()


# =============================================================================
# PART 2: USEFUL STANDARD LIBRARY MODULES
# =============================================================================
#
# Python comes with 200+ modules built in. Here are the most useful:

print("=" * 40)
print("PART 2: Standard library highlights")
print("=" * 40)

# --- os: Operating system interaction ---
import os
print(f"Current directory: {os.getcwd()}")
print(f"Files here: {os.listdir('.')[:5]}...")  # First 5 files
# os.path.join("folder", "file.txt") -> "folder/file.txt"
# os.path.exists("file.txt") -> True/False
# os.makedirs("new/folder", exist_ok=True)

# --- sys: Python system info ---
import sys
print(f"Python version: {sys.version.split()[0]}")
print(f"Platform: {sys.platform}")

# --- random: Random numbers ---
import random
print(f"Random int 1-10: {random.randint(1, 10)}")
print(f"Random choice: {random.choice(['apple', 'banana', 'cherry'])}")
print(f"Shuffled: {random.sample([1,2,3,4,5], 3)}")  # Pick 3 random

# --- collections: Advanced data structures ---
from collections import Counter, defaultdict

# Counter: count occurrences
words = "the cat sat on the mat the cat".split()
counts = Counter(words)
print(f"Word counts: {counts}")
print(f"Most common: {counts.most_common(2)}")

# defaultdict: dict with default values
dd = defaultdict(list)  # Missing keys auto-create empty lists
dd["fruits"].append("apple")
dd["fruits"].append("banana")
dd["vegs"].append("carrot")
print(f"defaultdict: {dict(dd)}")

# --- pathlib: Modern file path handling ---
from pathlib import Path
p = Path(".")
print(f"Python files: {list(p.glob('*.py'))[:3]}")

# --- itertools: Iteration tools ---
from itertools import chain, product
combined = list(chain([1, 2], [3, 4], [5]))
print(f"chain: {combined}")

print()


# =============================================================================
# PART 3: PIP - INSTALLING PACKAGES
# =============================================================================
#
# pip is Python's package manager. It downloads packages from PyPI
# (Python Package Index) - a repository of 500,000+ packages.
#
# COMMANDS (run in terminal, not Python):
#
#   pip install flask           Install a package
#   pip install flask==3.0.0    Install a specific version
#   pip install -r requirements.txt   Install from a file
#   pip uninstall flask         Remove a package
#   pip list                    Show installed packages
#   pip freeze                  Show installed + versions (for requirements.txt)
#   pip freeze > requirements.txt     Save dependencies to file
#
#
# requirements.txt is how you share dependencies:
#   flask==3.0.0
#   langchain==0.1.0
#   requests==2.31.0
#
# Someone else runs: pip install -r requirements.txt
# And gets the exact same packages. Reproducible environments!

print("=" * 40)
print("PART 3: pip (run these in terminal)")
print("=" * 40)
print("  pip install flask")
print("  pip list")
print("  pip freeze > requirements.txt")
print()


# =============================================================================
# PART 4: VIRTUAL ENVIRONMENTS
# =============================================================================
#
# Problem: Project A needs flask 2.0, Project B needs flask 3.0.
# If you install globally, they conflict.
#
# Solution: Virtual environments. Each project gets its OWN copy of Python
# and packages, completely isolated.
#
# COMMANDS:
#   python -m venv venv            Create a virtual environment called "venv"
#   source venv/bin/activate       Activate it (Linux/Mac)
#   venv\Scripts\activate          Activate it (Windows)
#   pip install flask              Now installs ONLY in this venv
#   deactivate                     Leave the virtual environment
#
# BEST PRACTICE:
#   1. Create a venv for EVERY project
#   2. Add "venv/" to .gitignore
#   3. Use requirements.txt to track dependencies
#   4. Never install packages globally (except pip itself)

print("=" * 40)
print("PART 4: Virtual environments")
print("=" * 40)
print("  python -m venv venv")
print("  source venv/bin/activate  (or venv\\Scripts\\activate on Windows)")
print("  pip install flask")
print("  pip freeze > requirements.txt")
print("  deactivate")
print()


# =============================================================================
# PART 5: CREATING YOUR OWN MODULES
# =============================================================================
#
# Any .py file is a module. If you have:
#   myproject/
#     main.py
#     helpers.py
#     utils/
#       __init__.py
#       math_utils.py
#
# In main.py:
#   from helpers import my_function
#   from utils.math_utils import calculate
#
# __init__.py makes a folder a "package" (can be empty).
#
# The if __name__ == "__main__" pattern:
#   Code inside this block ONLY runs when the file is executed directly.
#   It does NOT run when the file is imported as a module.

print("=" * 40)
print("PART 5: __name__ == '__main__'")
print("=" * 40)

def useful_function():
    return 42

# This only runs when you do: python this_file.py
# NOT when another file does: from this_file import useful_function
if __name__ == "__main__":
    print(f"  Running directly! Result: {useful_function()}")
    print(f"  __name__ = '{__name__}'")

# When imported: __name__ = 'ch8_modules_and_packages'
# When run directly: __name__ = '__main__'
print()


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Import:
#   import module
#   from module import thing
#   from module import thing as alias
#
# Useful stdlib:
#   os, sys, math, random, json, datetime, pathlib
#   collections (Counter, defaultdict), itertools
#
# pip:
#   pip install package
#   pip freeze > requirements.txt
#   pip install -r requirements.txt
#
# Virtual env:
#   python -m venv venv
#   source venv/bin/activate (or venv\Scripts\activate)
#   deactivate
#
# =============================================================================
