"""
=====================================================
 CHAPTER 9: PRACTICAL MINI-PROJECTS
=====================================================

Let's put everything together with real, useful programs.
Each project uses concepts from previous chapters.

  Project 1: Word Frequency Counter (files, dicts, sorting)
  Project 2: Simple CLI Todo App (lists, file I/O, loops)
  Project 3: API Data Fetcher (requests, JSON, error handling)
  Project 4: Password Generator (random, strings, functions)


INSTALL (for Project 3):
  pip install requests


HOW TO RUN:
  python ch9_practical_projects.py
"""

import os
import json
import random
import string


# =============================================================================
# PROJECT 1: WORD FREQUENCY COUNTER
# =============================================================================

print("=" * 60)
print("PROJECT 1: Word Frequency Counter")
print("=" * 60)

sample_text = """
Python is a great programming language. Python is easy to learn.
Many developers love Python because Python is versatile.
You can use Python for web development, data science, AI,
automation, and much more. Python has a huge community.
"""

def count_words(text: str) -> dict[str, int]:
    """Count word frequencies in a text string."""
    # Clean and split
    words = text.lower().replace(",", "").replace(".", "").split()
    # Count using a dict
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(counts: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Return the top N most frequent words."""
    sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:n]


counts = count_words(sample_text)
print(f"Total unique words: {len(counts)}")
print(f"Top 5 words:")
for word, count in top_words(counts, 5):
    bar = "#" * count
    print(f"  {word:>12}: {count:>2} {bar}")
print()


# =============================================================================
# PROJECT 2: CLI TODO APP
# =============================================================================

print("=" * 60)
print("PROJECT 2: CLI Todo App")
print("=" * 60)

TODO_FILE = "todos.json"


class TodoApp:
    """A simple todo list that saves to a JSON file."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.todos = self._load()

    def _load(self) -> list[dict]:
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.todos, f, indent=2)

    def add(self, task: str) -> dict:
        todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "done": False,
        }
        self.todos.append(todo)
        self._save()
        return todo

    def complete(self, todo_id: int) -> bool:
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["done"] = True
                self._save()
                return True
        return False

    def delete(self, todo_id: int) -> bool:
        before = len(self.todos)
        self.todos = [t for t in self.todos if t["id"] != todo_id]
        if len(self.todos) < before:
            self._save()
            return True
        return False

    def list_all(self):
        if not self.todos:
            print("  No todos!")
            return
        for todo in self.todos:
            status = "[x]" if todo["done"] else "[ ]"
            print(f"  {status} #{todo['id']}: {todo['task']}")


# Demo the todo app:
app = TodoApp(TODO_FILE)
app.add("Learn Python basics")
app.add("Build a Flask app")
app.add("Study LangChain")
app.complete(1)  # Complete first task

print("Todo list:")
app.list_all()

app.delete(2)
print("\nAfter deleting #2:")
app.list_all()
print()

# Cleanup
os.remove(TODO_FILE)


# =============================================================================
# PROJECT 3: API DATA FETCHER
# =============================================================================

print("=" * 60)
print("PROJECT 3: API Data Fetcher")
print("=" * 60)

try:
    import requests

    def fetch_random_user() -> dict:
        """Fetch a random user from a free public API."""
        response = requests.get("https://randomuser.me/api/")
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        user = data["results"][0]
        return {
            "name": f"{user['name']['first']} {user['name']['last']}",
            "email": user["email"],
            "country": user["location"]["country"],
            "age": user["dob"]["age"],
        }

    # Fetch 3 random users:
    print("Random users from API:")
    for i in range(3):
        try:
            user = fetch_random_user()
            print(f"  {i+1}. {user['name']} ({user['age']}) - {user['country']}")
            print(f"     Email: {user['email']}")
        except requests.RequestException as e:
            print(f"  API error: {e}")

except ImportError:
    print("  (Skipped - install 'requests' to try this: pip install requests)")

print()


# =============================================================================
# PROJECT 4: PASSWORD GENERATOR
# =============================================================================

print("=" * 60)
print("PROJECT 4: Password Generator")
print("=" * 60)


def generate_password(
    length: int = 16,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
) -> str:
    """Generate a random password with specified character types."""
    chars = ""
    required = []  # Ensure at least one of each type

    if uppercase:
        chars += string.ascii_uppercase
        required.append(random.choice(string.ascii_uppercase))
    if lowercase:
        chars += string.ascii_lowercase
        required.append(random.choice(string.ascii_lowercase))
    if digits:
        chars += string.digits
        required.append(random.choice(string.digits))
    if symbols:
        chars += "!@#$%^&*()-_=+"
        required.append(random.choice("!@#$%^&*()-_=+"))

    if not chars:
        raise ValueError("At least one character type must be enabled")

    # Fill remaining length with random chars
    remaining = length - len(required)
    password = required + [random.choice(chars) for _ in range(remaining)]
    random.shuffle(password)  # Shuffle so required chars aren't at the start

    return "".join(password)


def check_strength(password: str) -> str:
    """Rate password strength."""
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in "!@#$%^&*()-_=+" for c in password): score += 1

    if score <= 2: return "Weak"
    if score <= 4: return "Medium"
    return "Strong"


# Generate some passwords:
for length in [8, 12, 16, 24]:
    pw = generate_password(length=length)
    strength = check_strength(pw)
    print(f"  Length {length:>2}: {pw}  [{strength}]")

# Custom: digits only (PIN)
pin = generate_password(length=6, uppercase=False, lowercase=False, symbols=False)
print(f"  PIN:      {pin}")

# Custom: no symbols
safe = generate_password(length=12, symbols=False)
print(f"  No symbols: {safe}")
print()


# =============================================================================
# WHAT THESE PROJECTS USED
# =============================================================================
#
# Project 1 (Word Counter):
#   Strings, dicts, sorting, lambda, functions
#
# Project 2 (Todo App):
#   Classes, file I/O, JSON, lists, methods
#
# Project 3 (API Fetcher):
#   External packages (requests), JSON, error handling, dicts
#
# Project 4 (Password Generator):
#   random, string module, functions with defaults, list comprehensions
#
# =============================================================================
