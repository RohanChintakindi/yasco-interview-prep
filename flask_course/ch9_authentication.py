"""
=====================================================
 CHAPTER 9: AUTHENTICATION (LOGIN, REGISTER, SESSIONS)
=====================================================

WHAT IS AUTHENTICATION?
-----------------------
Authentication = "Who are you?"
Authorization = "What are you allowed to do?"

This chapter covers authentication:
  - User registration (create account)
  - Login (prove who you are)
  - Sessions (stay logged in across pages)
  - Logout (end the session)
  - Protecting routes (only logged-in users can access)


HOW SESSIONS WORK
-----------------
HTTP is STATELESS. The server doesn't know if two requests come from
the same person. Sessions solve this:

  1. User logs in (sends username + password)
  2. Server creates a SESSION (stored on the server)
  3. Server sends back a SESSION COOKIE (small token)
  4. Browser sends the cookie with EVERY request
  5. Server reads the cookie -> finds the session -> knows who you are

  Browser                          Server
    |-- POST /login (user+pass) -->|
    |                              | (creates session)
    |<-- Set-Cookie: session=abc --|
    |                              |
    |-- GET /dashboard            -|
    |   Cookie: session=abc        | (reads cookie -> finds session -> it's Chint!)
    |<-- "Welcome, Chint!"      --|

Flask handles sessions via the `session` object (a dict-like cookie).


INSTALL:
  pip install flask flask-sqlalchemy werkzeug


HOW TO RUN:
  python ch9_authentication.py
"""

from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
db = SQLAlchemy(app)


# =============================================================================
# USER MODEL
# =============================================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """
        NEVER store passwords as plain text!
        generate_password_hash() creates a salted hash.
        Even if the database is stolen, passwords can't be read.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password_hash, password)


# =============================================================================
# LOGIN REQUIRED DECORATOR
# =============================================================================
#
# This decorator protects routes so only logged-in users can access them.
# If not logged in, redirects to the login page.

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# =============================================================================
# TEMPLATES
# =============================================================================

BASE_TEMPLATE = """<!DOCTYPE html>
<html><head><title>{% block title %}Auth App{% endblock %}</title>
<style>
body{font-family:Arial;max-width:600px;margin:40px auto;padding:0 20px}
form{background:#f9f9f9;padding:20px;border-radius:8px}
label{display:block;margin:10px 0 5px;font-weight:bold}
input{width:100%;padding:8px;margin-bottom:10px;box-sizing:border-box;border:1px solid #ddd;border-radius:4px}
button{background:#3498db;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer}
nav{margin-bottom:20px} nav a{margin-right:15px}
.flash{padding:10px;margin:10px 0;border-radius:4px;background:#f8d7da;color:#721c24}
.success{background:#d4edda;color:#155724}
</style></head><body>
<nav>
{% if session.get('user_id') %}
    <a href="/">Home</a> <a href="/dashboard">Dashboard</a> <a href="/profile">Profile</a> <a href="/logout">Logout</a>
    <span style="float:right">Logged in as <strong>{{ session.get('username') }}</strong></span>
{% else %}
    <a href="/">Home</a> <a href="/login">Login</a> <a href="/register">Register</a>
{% endif %}
</nav>
{% with messages = get_flashed_messages() %}{% for msg in messages %}<div class="flash success">{{ msg }}</div>{% endfor %}{% endwith %}
{% block content %}{% endblock %}
</body></html>"""


# =============================================================================
# ROUTES
# =============================================================================

@app.route("/")
def index():
    return render_template_string(BASE_TEMPLATE + """
    {% block content %}
    <h1>Authentication Demo</h1>
    {% if session.get('user_id') %}
        <p>Welcome back, {{ session.username }}! <a href="/dashboard">Go to dashboard</a></p>
    {% else %}
        <p><a href="/register">Register</a> or <a href="/login">Login</a> to get started.</p>
    {% endif %}
    {% endblock %}
    """)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Validation
        if len(username) < 3 or len(password) < 6:
            flash("Username must be 3+ chars, password 6+ chars.")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already taken.")
            return redirect(url_for("register"))

        # Create user with HASHED password
        user = User(username=username, email=email)
        user.set_password(password)  # Stores hash, NOT plain text!

        db.session.add(user)
        db.session.commit()

        flash(f"Account created! Please log in.")
        return redirect(url_for("login"))

    return render_template_string(BASE_TEMPLATE + """
    {% block content %}
    <h1>Register</h1>
    <form method="POST">
        <label>Username:</label><input name="username" required>
        <label>Email:</label><input type="email" name="email" required>
        <label>Password:</label><input type="password" name="password" required>
        <button type="submit">Register</button>
    </form>
    {% endblock %}
    """)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # SUCCESS: Create a session
            session["user_id"] = user.id
            session["username"] = user.username
            # Now session["user_id"] is set -> login_required will let them through
            flash(f"Welcome back, {user.username}!")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("login"))

    return render_template_string(BASE_TEMPLATE + """
    {% block content %}
    <h1>Login</h1>
    <form method="POST">
        <label>Username:</label><input name="username" required>
        <label>Password:</label><input type="password" name="password" required>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="/register">Register</a></p>
    {% endblock %}
    """)


@app.route("/logout")
def logout():
    """Clear the session -> user is logged out."""
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required  # This route requires authentication!
def dashboard():
    return render_template_string(BASE_TEMPLATE + """
    {% block content %}
    <h1>Dashboard</h1>
    <p>This page is PROTECTED. Only logged-in users can see it.</p>
    <p>User ID: {{ session.user_id }}</p>
    <p>Username: {{ session.username }}</p>
    {% endblock %}
    """)


@app.route("/profile")
@login_required
def profile():
    user = db.session.get(User, session["user_id"])
    return render_template_string(BASE_TEMPLATE + """
    {% block content %}
    <h1>{{ user.username }}'s Profile</h1>
    <p>Email: {{ user.email }}</p>
    <p>Password hash: {{ user.password_hash[:30] }}... (never stored as plain text!)</p>
    {% endblock %}
    """, user=user)


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Password hashing:
#   from werkzeug.security import generate_password_hash, check_password_hash
#   hash = generate_password_hash("password123")
#   check_password_hash(hash, "password123")  -> True
#
# Session:
#   session["user_id"] = 1            -> set session data
#   user_id = session.get("user_id")  -> read session data
#   session.clear()                   -> destroy session (logout)
#
# Protect routes:
#   @login_required
#   def my_route(): ...
#
# =============================================================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
