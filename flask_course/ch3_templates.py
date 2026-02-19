"""
=====================================================
 CHAPTER 3: TEMPLATES (JINJA2)
=====================================================

THE PROBLEM
-----------
In Chapters 1-2, we returned HTML as Python strings:
  return "<h1>Hello</h1><p>Welcome</p>"

This is awful for real apps because:
  1. HTML mixed with Python is unreadable
  2. No syntax highlighting for HTML inside strings
  3. Can't reuse layouts (header/footer on every page)
  4. Hard to pass dynamic data safely (XSS vulnerabilities)


THE SOLUTION: TEMPLATES
-----------------------
Templates are separate HTML files with special {{ }} placeholders.
Flask uses Jinja2 as its template engine.

Your Python code passes DATA to the template.
The template handles the PRESENTATION.

This is called "separation of concerns":
  - Python (logic):  WHAT data to show
  - Template (HTML):  HOW to show it


HOW JINJA2 WORKS
-----------------
Jinja2 has its own mini-language inside HTML:

  {{ variable }}       -> Output a variable's value
  {% if condition %}   -> Logic (if/else/for)
  {# comment #}       -> Comments (not rendered)
  {% extends "base" %} -> Template inheritance


SETUP: Create a "templates" folder next to this file:
  flask_course/
    ch3_templates.py
    templates/
      base.html
      index.html
      profile.html
      products.html


HOW TO RUN:
  python ch3_templates.py
  Then open http://127.0.0.1:5000
"""

from flask import Flask, render_template

app = Flask(__name__)


# =============================================================================
# SETUP: CREATE TEMPLATE FILES
# =============================================================================
# We'll create the template files programmatically so you can just run this.

import os

template_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(template_dir, exist_ok=True)


# --- base.html: The master layout ---
with open(os.path.join(template_dir, "base.html"), "w") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Flask App{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        nav { background: #2c3e50; padding: 10px 20px; margin: -20px -20px 20px; }
        nav a { color: white; text-decoration: none; margin-right: 15px; }
        nav a:hover { text-decoration: underline; }
        .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .tag { background: #3498db; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.8em; }
    </style>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/profile/Chint">Profile</a>
        <a href="/products">Products</a>
    </nav>

    {% block content %}
    <!-- Child templates fill this in -->
    {% endblock %}
</body>
</html>
""")


# --- index.html: Extends base, fills in content ---
with open(os.path.join(template_dir, "index.html"), "w") as f:
    f.write("""{% extends "base.html" %}

{% block title %}Home - Flask App{% endblock %}

{% block content %}
<h1>Welcome, {{ name }}!</h1>
<p>Today is {{ day }}.</p>
<p>You have {{ message_count }} messages.</p>

{# This is a Jinja2 comment - it won't appear in the HTML #}

{% if message_count > 0 %}
    <p style="color: green;">You have new messages!</p>
{% else %}
    <p style="color: gray;">No new messages.</p>
{% endif %}
{% endblock %}
""")


# --- profile.html: Using variables and conditionals ---
with open(os.path.join(template_dir, "profile.html"), "w") as f:
    f.write("""{% extends "base.html" %}

{% block title %}{{ user.name }}'s Profile{% endblock %}

{% block content %}
<h1>{{ user.name }}'s Profile</h1>

<div class="card">
    <p><strong>Name:</strong> {{ user.name }}</p>
    <p><strong>Email:</strong> {{ user.email }}</p>
    <p><strong>Bio:</strong> {{ user.bio | default("No bio yet.") }}</p>
</div>

<h2>Skills</h2>
{% if user.skills %}
    <ul>
    {% for skill in user.skills %}
        <li>{{ skill }}</li>
    {% endfor %}
    </ul>
{% else %}
    <p>No skills listed.</p>
{% endif %}
{% endblock %}
""")


# --- products.html: Looping through data ---
with open(os.path.join(template_dir, "products.html"), "w") as f:
    f.write("""{% extends "base.html" %}

{% block title %}Products{% endblock %}

{% block content %}
<h1>Products ({{ products | length }} items)</h1>

{% for product in products %}
<div class="card">
    <h3>{{ product.name }}</h3>
    <p>{{ product.description }}</p>
    <p><strong>${{ "%.2f" | format(product.price) }}</strong></p>

    {% for tag in product.tags %}
        <span class="tag">{{ tag }}</span>
    {% endfor %}

    {% if product.in_stock %}
        <p style="color: green;">In Stock</p>
    {% else %}
        <p style="color: red;">Out of Stock</p>
    {% endif %}
</div>
{% endfor %}

{% if not products %}
    <p>No products available.</p>
{% endif %}
{% endblock %}
""")


# =============================================================================
# ROUTES
# =============================================================================

@app.route("/")
def index():
    """
    render_template() loads an HTML file from the templates/ folder
    and fills in the {{ }} placeholders with the values you pass.

    Template variables become available inside the HTML:
      {{ name }}  -> "Chint"
      {{ day }}   -> "Monday"
    """
    return render_template("index.html",
        name="Chint",
        day="Monday",
        message_count=5,
    )


@app.route("/profile/<username>")
def profile(username):
    """
    You can pass any Python object to templates: dicts, lists, etc.
    The template accesses dict keys with dot notation: {{ user.name }}
    """
    user = {
        "name": username,
        "email": f"{username.lower()}@example.com",
        "bio": "Learning Flask and building cool things!",
        "skills": ["Python", "Flask", "LangChain", "JavaScript"],
    }
    return render_template("profile.html", user=user)


@app.route("/products")
def products():
    """
    Passing a list of dicts - the template loops through them with {% for %}.
    """
    product_list = [
        {"name": "Python Course", "description": "Learn Python from scratch",
         "price": 29.99, "tags": ["programming", "beginner"], "in_stock": True},
        {"name": "Flask Course", "description": "Build web apps with Flask",
         "price": 39.99, "tags": ["web", "backend"], "in_stock": True},
        {"name": "AI Masterclass", "description": "LangChain, LangGraph, RAG",
         "price": 79.99, "tags": ["AI", "advanced"], "in_stock": False},
    ]
    return render_template("products.html", products=product_list)


# =============================================================================
# JINJA2 CHEAT SHEET (used inside templates)
# =============================================================================
#
# OUTPUT VARIABLE:
#   {{ name }}                    -> prints the value
#   {{ user.email }}              -> dict/object attribute
#   {{ items[0] }}                -> list indexing
#
# FILTERS (transform values):
#   {{ name | upper }}            -> "CHINT"
#   {{ name | lower }}            -> "chint"
#   {{ name | length }}           -> 5
#   {{ bio | default("N/A") }}    -> "N/A" if bio is empty
#   {{ price | round(2) }}        -> 29.99
#   {{ items | join(", ") }}      -> "a, b, c"
#
# CONDITIONALS:
#   {% if score > 90 %}
#       <p>Excellent!</p>
#   {% elif score > 60 %}
#       <p>Good</p>
#   {% else %}
#       <p>Needs work</p>
#   {% endif %}
#
# LOOPS:
#   {% for item in items %}
#       <p>{{ item.name }}</p>
#   {% endfor %}
#
#   Loop variables:
#     {{ loop.index }}    -> 1, 2, 3... (1-based)
#     {{ loop.index0 }}   -> 0, 1, 2... (0-based)
#     {{ loop.first }}    -> True on first iteration
#     {{ loop.last }}     -> True on last iteration
#
# TEMPLATE INHERITANCE:
#   base.html:   {% block content %}{% endblock %}
#   child.html:  {% extends "base.html" %}
#                {% block content %}<h1>My Page</h1>{% endblock %}
#
# =============================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
