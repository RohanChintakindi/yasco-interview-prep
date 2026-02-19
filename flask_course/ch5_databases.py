"""
=====================================================
 CHAPTER 5: DATABASES WITH FLASK-SQLALCHEMY
=====================================================

THE PROBLEM
-----------
So far our data disappears when the server restarts. We need a DATABASE
to store data permanently: users, posts, products, etc.

Flask doesn't have a built-in database system (unlike Django).
Instead, you choose your own. The most popular choice is:

  Flask-SQLAlchemy = Flask + SQLAlchemy (Python's #1 database toolkit)

SQLAlchemy is an ORM (Object-Relational Mapper). It lets you:
  - Define database tables as Python CLASSES
  - Query data using Python CODE instead of raw SQL
  - Works with SQLite, PostgreSQL, MySQL, etc.

  Instead of:  SELECT * FROM users WHERE name = 'Chint'
  You write:   User.query.filter_by(name='Chint').first()


WHAT IS SQLite?
---------------
SQLite is a lightweight database that stores everything in a single file.
No server needed. Perfect for learning and small apps.

  PostgreSQL = industrial database server (production)
  SQLite = a database in a single file (development, learning)


INSTALL:
  pip install flask-sqlalchemy


HOW TO RUN:
  python ch5_databases.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "dev-secret"

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# Tell Flask-SQLAlchemy where the database file lives.
# sqlite:///site.db means: SQLite database, file called "site.db" in current dir.

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# Create the SQLAlchemy database object
# This "db" object is how you interact with the database from Flask.
db = SQLAlchemy(app)


# =============================================================================
# MODELS (DATABASE TABLES)
# =============================================================================
#
# A MODEL is a Python class that maps to a database TABLE.
# Each class attribute becomes a COLUMN in the table.
#
# class User -> table "user" with columns: id, username, email, created_at
#
# Think of it like a spreadsheet:
#   The CLASS is the spreadsheet (defines columns)
#   Each INSTANCE is a row in the spreadsheet

class User(db.Model):
    """
    Each User instance = one row in the 'user' table.

    db.Column() defines a column:
      type:         Integer, String(length), Text, Float, Boolean, DateTime
      primary_key:  This column uniquely identifies each row (auto-incrementing)
      unique:       No two rows can have the same value
      nullable:     Can this column be empty? (False = required)
      default:      Default value if none provided
    """
    id = db.Column(db.Integer, primary_key=True)           # Auto-incrementing ID
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text, default="")                   # Optional, defaults to ""
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # RELATIONSHIP: One user has many posts
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    """A blog post. Each post belongs to one user (foreign key)."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FOREIGN KEY: links this post to a user
    # "user.id" means the "id" column of the "user" table
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"


# =============================================================================
# CREATE TABLES & SEED DATA
# =============================================================================

template_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(template_dir, exist_ok=True)

# Create templates for this chapter
with open(os.path.join(template_dir, "db_base.html"), "w") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}DB App{% endblock %}</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 40px auto; padding: 0 20px; }
        nav { margin-bottom: 20px; } nav a { margin-right: 15px; }
        .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        form { background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0; }
        label { display: block; margin: 10px 0 5px; font-weight: bold; }
        input, textarea { width: 100%; padding: 8px; margin-bottom: 10px; box-sizing: border-box; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin-right: 5px; }
        .delete { background: #e74c3c; }
        .flash { padding: 10px; margin: 10px 0; border-radius: 4px; background: #d4edda; color: #155724; }
        .meta { color: #888; font-size: 0.9em; }
    </style>
</head>
<body>
    <nav>
        <a href="/db">Users</a>
        <a href="/db/add-user">Add User</a>
        <a href="/db/posts">All Posts</a>
    </nav>
    {% with messages = get_flashed_messages() %}
        {% for message in messages %}<div class="flash">{{ message }}</div>{% endfor %}
    {% endwith %}
    {% block content %}{% endblock %}
</body></html>
""")

with open(os.path.join(template_dir, "db_users.html"), "w") as f:
    f.write("""{% extends "db_base.html" %}
{% block content %}
<h1>Users ({{ users | length }})</h1>
{% for user in users %}
<div class="card">
    <h3><a href="/db/user/{{ user.id }}">{{ user.username }}</a></h3>
    <p>{{ user.email }}</p>
    <p class="meta">Joined: {{ user.created_at.strftime('%Y-%m-%d') }} | Posts: {{ user.posts | length }}</p>
</div>
{% endfor %}
{% endblock %}
""")

with open(os.path.join(template_dir, "db_user_detail.html"), "w") as f:
    f.write("""{% extends "db_base.html" %}
{% block content %}
<h1>{{ user.username }}</h1>
<p>Email: {{ user.email }}</p>
<p>Bio: {{ user.bio or 'No bio' }}</p>
<p class="meta">Joined: {{ user.created_at.strftime('%Y-%m-%d %H:%M') }}</p>

<h2>Posts by {{ user.username }}</h2>
{% for post in user.posts %}
<div class="card">
    <h3>{{ post.title }}</h3>
    <p>{{ post.content }}</p>
    <p class="meta">{{ post.created_at.strftime('%Y-%m-%d') }}</p>
</div>
{% endfor %}

<h3>New Post</h3>
<form method="POST" action="/db/user/{{ user.id }}/post">
    <label>Title:</label><input type="text" name="title" required>
    <label>Content:</label><textarea name="content" rows="3" required></textarea>
    <button type="submit">Add Post</button>
</form>
{% endblock %}
""")

with open(os.path.join(template_dir, "db_add_user.html"), "w") as f:
    f.write("""{% extends "db_base.html" %}
{% block content %}
<h1>Add User</h1>
<form method="POST">
    <label>Username:</label><input type="text" name="username" required>
    <label>Email:</label><input type="email" name="email" required>
    <label>Bio:</label><textarea name="bio" rows="2"></textarea>
    <button type="submit">Create User</button>
</form>
{% endblock %}
""")

with open(os.path.join(template_dir, "db_posts.html"), "w") as f:
    f.write("""{% extends "db_base.html" %}
{% block content %}
<h1>All Posts</h1>
{% for post in posts %}
<div class="card">
    <h3>{{ post.title }}</h3>
    <p>{{ post.content }}</p>
    <p class="meta">By <a href="/db/user/{{ post.author.id }}">{{ post.author.username }}</a> on {{ post.created_at.strftime('%Y-%m-%d') }}</p>
</div>
{% endfor %}
{% endblock %}
""")


# =============================================================================
# ROUTES - CRUD OPERATIONS
# =============================================================================
# CRUD = Create, Read, Update, Delete - the four basic database operations

@app.route("/db")
def list_users():
    """READ: Get all users from the database."""
    users = User.query.all()  # SELECT * FROM user
    return render_template("db_users.html", users=users)


@app.route("/db/user/<int:user_id>")
def user_detail(user_id):
    """READ: Get one user by ID."""
    user = db.session.get(User, user_id)  # SELECT * FROM user WHERE id = ?
    if not user:
        return "User not found", 404
    return render_template("db_user_detail.html", user=user)


@app.route("/db/add-user", methods=["GET", "POST"])
def add_user():
    """CREATE: Add a new user to the database."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        bio = request.form.get("bio", "")

        # Create a new User object
        new_user = User(username=username, email=email, bio=bio)

        # Add to database
        db.session.add(new_user)    # Stage the change
        db.session.commit()         # Save to database

        flash(f"User {username} created!")
        return redirect(url_for("list_users"))

    return render_template("db_add_user.html")


@app.route("/db/user/<int:user_id>/post", methods=["POST"])
def add_post(user_id):
    """CREATE: Add a post for a specific user."""
    title = request.form.get("title")
    content = request.form.get("content")

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    flash(f"Post '{title}' created!")
    return redirect(url_for("user_detail", user_id=user_id))


@app.route("/db/posts")
def all_posts():
    """READ: Get all posts, newest first."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("db_posts.html", posts=posts)


@app.route("/db/user/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """DELETE: Remove a user and their posts."""
    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.username} deleted.")
    return redirect(url_for("list_users"))


# =============================================================================
# SQLALCHEMY QUERY CHEAT SHEET
# =============================================================================
#
# Get all:        User.query.all()
# Get by ID:      db.session.get(User, 1)
# Filter:         User.query.filter_by(username="chint").first()
# Filter (adv):   User.query.filter(User.email.contains("@gmail")).all()
# Order by:       User.query.order_by(User.created_at.desc()).all()
# Limit:          User.query.limit(10).all()
# Count:          User.query.count()
#
# Create:         db.session.add(new_user); db.session.commit()
# Update:         user.email = "new@email.com"; db.session.commit()
# Delete:         db.session.delete(user); db.session.commit()
#
# =============================================================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

        # Seed some data if the database is empty
        if User.query.count() == 0:
            u1 = User(username="chint", email="chint@example.com", bio="Flask learner")
            u2 = User(username="alice", email="alice@example.com", bio="Python dev")
            db.session.add_all([u1, u2])
            db.session.commit()

            p1 = Post(title="Hello Flask!", content="Learning Flask is fun.", user_id=u1.id)
            p2 = Post(title="SQLAlchemy Tips", content="ORMs make databases easy.", user_id=u1.id)
            p3 = Post(title="Python Love", content="Python is my favorite language.", user_id=u2.id)
            db.session.add_all([p1, p2, p3])
            db.session.commit()
            print("Database seeded with sample data!")

    app.run(debug=True, port=5000)
