"""
=====================================================
 CHAPTER 10: FINAL PROJECT - BOOKMARK MANAGER
=====================================================

THE CAPSTONE
------------
A full Flask web app that combines everything:
  - Routes & URL parameters (Ch1-2)
  - Templates with Jinja2 (Ch3)
  - Forms & validation (Ch4)
  - Database with SQLAlchemy (Ch5)
  - REST API (Ch6)
  - Blueprints structure (Ch7)
  - Middleware & error handling (Ch8)
  - Authentication (Ch9)

THE APP: BOOKMARK MANAGER
  - Users can register and log in
  - Save bookmarks (URL + title + tags)
  - View, edit, and delete bookmarks
  - Search bookmarks by title or tag
  - REST API for programmatic access
  - All data persists in SQLite


HOW TO RUN:
  pip install flask flask-sqlalchemy
  python ch10_project_full_app.py
  Open http://127.0.0.1:5000
"""

from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session, flash, jsonify, abort, g
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import time

# =============================================================================
# APP SETUP
# =============================================================================

app = Flask(__name__)
app.secret_key = "bookmark-manager-dev-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"
db = SQLAlchemy(app)


# =============================================================================
# MODELS
# =============================================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookmarks = db.relationship("Bookmark", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, default="")
    tags = db.Column(db.String(200), default="")  # Comma-separated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


# =============================================================================
# MIDDLEWARE
# =============================================================================

@app.before_request
def load_user():
    g.user = None
    if "user_id" in session:
        g.user = db.session.get(User, session["user_id"])


@app.before_request
def timer_start():
    g.start = time.time()


@app.after_request
def timer_end(response):
    if hasattr(g, "start"):
        response.headers["X-Response-Time"] = f"{time.time() - g.start:.4f}s"
    return response


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.user:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# =============================================================================
# TEMPLATE
# =============================================================================

LAYOUT = """<!DOCTYPE html>
<html><head><title>{% block title %}Bookmarks{% endblock %}</title>
<style>
*{box-sizing:border-box}
body{font-family:'Segoe UI',Arial,sans-serif;max-width:900px;margin:0 auto;padding:20px;background:#f5f5f5}
nav{background:#2c3e50;padding:12px 20px;border-radius:8px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center}
nav a{color:#ecf0f1;text-decoration:none;margin-right:15px;font-size:0.95em}
nav a:hover{text-decoration:underline}
.nav-user{color:#bdc3c7;font-size:0.9em}
.container{background:white;padding:25px;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.1)}
h1{color:#2c3e50;margin-top:0}
form{margin:20px 0}
label{display:block;margin:8px 0 4px;font-weight:600;color:#555}
input,textarea{width:100%;padding:10px;border:1px solid #ddd;border-radius:4px;margin-bottom:8px}
button{background:#3498db;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;margin-right:5px}
button:hover{background:#2980b9}
.btn-danger{background:#e74c3c}
.btn-danger:hover{background:#c0392b}
.card{border:1px solid #e0e0e0;padding:15px;margin:10px 0;border-radius:6px;background:white}
.card h3{margin:0 0 5px}
.card h3 a{color:#2c3e50;text-decoration:none}
.card h3 a:hover{color:#3498db}
.meta{color:#999;font-size:0.85em;margin:5px 0}
.tag{display:inline-block;background:#3498db;color:white;padding:2px 8px;border-radius:12px;font-size:0.8em;margin:2px}
.flash{padding:12px;margin:10px 0;border-radius:4px;background:#d4edda;color:#155724;border:1px solid #c3e6cb}
.flash.error{background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.search-form{display:flex;gap:10px;margin:15px 0}
.search-form input{flex:1}
.search-form button{white-space:nowrap}
.actions{margin-top:10px}
.empty{text-align:center;padding:40px;color:#999}
</style></head><body>
<nav>
<div>
    <a href="/">Home</a>
    {% if g.user %}<a href="/bookmarks">My Bookmarks</a><a href="/bookmarks/add">Add Bookmark</a>{% endif %}
</div>
<div>
    {% if g.user %}
        <span class="nav-user">{{ g.user.username }}</span> <a href="/logout">Logout</a>
    {% else %}
        <a href="/login">Login</a> <a href="/register">Register</a>
    {% endif %}
</div>
</nav>
{% with messages = get_flashed_messages() %}{% for msg in messages %}<div class="flash">{{ msg }}</div>{% endfor %}{% endwith %}
<div class="container">{% block content %}{% endblock %}</div>
</body></html>"""


# =============================================================================
# AUTH ROUTES
# =============================================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if len(username) < 3 or len(password) < 6:
            flash("Username (3+) and password (6+) required.")
            return redirect(url_for("register"))
        if User.query.filter_by(username=username).first():
            flash("Username taken.")
            return redirect(url_for("register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
        return redirect(url_for("login"))

    return render_template_string(LAYOUT + """{% block content %}
    <h1>Register</h1>
    <form method="POST">
        <label>Username:</label><input name="username" required>
        <label>Email:</label><input type="email" name="email" required>
        <label>Password:</label><input type="password" name="password" required>
        <button>Register</button>
    </form>{% endblock %}""")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user and user.check_password(request.form.get("password")):
            session["user_id"] = user.id
            flash(f"Welcome, {user.username}!")
            return redirect(url_for("bookmarks_list"))
        flash("Invalid credentials.")
        return redirect(url_for("login"))

    return render_template_string(LAYOUT + """{% block content %}
    <h1>Login</h1>
    <form method="POST">
        <label>Username:</label><input name="username" required>
        <label>Password:</label><input type="password" name="password" required>
        <button>Login</button>
    </form>
    <p>No account? <a href="/register">Register</a></p>{% endblock %}""")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("index"))


# =============================================================================
# BOOKMARK ROUTES (CRUD)
# =============================================================================

@app.route("/")
def index():
    return render_template_string(LAYOUT + """{% block content %}
    <h1>Bookmark Manager</h1>
    {% if g.user %}
        <p>Welcome, {{ g.user.username }}! <a href="/bookmarks">View your bookmarks</a></p>
    {% else %}
        <p>Save, organize, and search your bookmarks.</p>
        <p><a href="/login">Login</a> or <a href="/register">Register</a> to get started.</p>
    {% endif %}{% endblock %}""")


@app.route("/bookmarks")
@login_required
def bookmarks_list():
    search = request.args.get("q", "").strip()
    if search:
        bookmarks = Bookmark.query.filter(
            Bookmark.user_id == g.user.id,
            (Bookmark.title.contains(search) | Bookmark.tags.contains(search))
        ).order_by(Bookmark.created_at.desc()).all()
    else:
        bookmarks = Bookmark.query.filter_by(user_id=g.user.id).order_by(Bookmark.created_at.desc()).all()

    return render_template_string(LAYOUT + """{% block content %}
    <h1>My Bookmarks ({{ bookmarks|length }})</h1>
    <div class="search-form">
        <form method="GET" style="display:flex;gap:10px;width:100%;margin:0">
            <input name="q" placeholder="Search by title or tag..." value="{{ search }}">
            <button>Search</button>
            {% if search %}<a href="/bookmarks"><button type="button">Clear</button></a>{% endif %}
        </form>
    </div>
    {% for b in bookmarks %}
    <div class="card">
        <h3><a href="{{ b.url }}" target="_blank">{{ b.title }}</a></h3>
        <p class="meta">{{ b.url }}</p>
        {% if b.description %}<p>{{ b.description }}</p>{% endif %}
        {% for tag in b.tag_list() %}<span class="tag">{{ tag }}</span>{% endfor %}
        <p class="meta">Added {{ b.created_at.strftime('%Y-%m-%d') }}</p>
        <div class="actions">
            <a href="/bookmarks/{{ b.id }}/edit"><button>Edit</button></a>
            <form method="POST" action="/bookmarks/{{ b.id }}/delete" style="display:inline">
                <button class="btn-danger" onclick="return confirm('Delete this bookmark?')">Delete</button>
            </form>
        </div>
    </div>
    {% else %}
    <div class="empty">
        <p>No bookmarks {% if search %}matching "{{ search }}"{% endif %}.</p>
        <a href="/bookmarks/add"><button>Add your first bookmark</button></a>
    </div>
    {% endfor %}{% endblock %}""", bookmarks=bookmarks, search=search)


@app.route("/bookmarks/add", methods=["GET", "POST"])
@login_required
def bookmark_add():
    if request.method == "POST":
        bm = Bookmark(
            title=request.form["title"],
            url=request.form["url"],
            description=request.form.get("description", ""),
            tags=request.form.get("tags", ""),
            user_id=g.user.id,
        )
        db.session.add(bm)
        db.session.commit()
        flash(f"Bookmark '{bm.title}' saved!")
        return redirect(url_for("bookmarks_list"))

    return render_template_string(LAYOUT + """{% block content %}
    <h1>Add Bookmark</h1>
    <form method="POST">
        <label>Title:</label><input name="title" required>
        <label>URL:</label><input name="url" type="url" required placeholder="https://...">
        <label>Description:</label><textarea name="description" rows="2"></textarea>
        <label>Tags (comma-separated):</label><input name="tags" placeholder="python, tutorial, flask">
        <button>Save Bookmark</button>
    </form>{% endblock %}""")


@app.route("/bookmarks/<int:bm_id>/edit", methods=["GET", "POST"])
@login_required
def bookmark_edit(bm_id):
    bm = Bookmark.query.get_or_404(bm_id)
    if bm.user_id != g.user.id:
        abort(403)

    if request.method == "POST":
        bm.title = request.form["title"]
        bm.url = request.form["url"]
        bm.description = request.form.get("description", "")
        bm.tags = request.form.get("tags", "")
        db.session.commit()
        flash("Bookmark updated!")
        return redirect(url_for("bookmarks_list"))

    return render_template_string(LAYOUT + """{% block content %}
    <h1>Edit Bookmark</h1>
    <form method="POST">
        <label>Title:</label><input name="title" value="{{ bm.title }}" required>
        <label>URL:</label><input name="url" type="url" value="{{ bm.url }}" required>
        <label>Description:</label><textarea name="description" rows="2">{{ bm.description }}</textarea>
        <label>Tags:</label><input name="tags" value="{{ bm.tags }}">
        <button>Save Changes</button>
    </form>{% endblock %}""", bm=bm)


@app.route("/bookmarks/<int:bm_id>/delete", methods=["POST"])
@login_required
def bookmark_delete(bm_id):
    bm = Bookmark.query.get_or_404(bm_id)
    if bm.user_id != g.user.id:
        abort(403)
    db.session.delete(bm)
    db.session.commit()
    flash("Bookmark deleted.")
    return redirect(url_for("bookmarks_list"))


# =============================================================================
# REST API
# =============================================================================

@app.route("/api/bookmarks", methods=["GET"])
@login_required
def api_bookmarks():
    bms = Bookmark.query.filter_by(user_id=g.user.id).all()
    return jsonify([{
        "id": b.id, "title": b.title, "url": b.url,
        "description": b.description, "tags": b.tag_list(),
        "created_at": b.created_at.isoformat(),
    } for b in bms])


@app.route("/api/bookmarks", methods=["POST"])
@login_required
def api_bookmark_create():
    data = request.json
    if not data or not data.get("title") or not data.get("url"):
        return jsonify({"error": "title and url required"}), 400
    bm = Bookmark(
        title=data["title"], url=data["url"],
        description=data.get("description", ""),
        tags=",".join(data.get("tags", [])),
        user_id=g.user.id,
    )
    db.session.add(bm)
    db.session.commit()
    return jsonify({"id": bm.id, "title": bm.title}), 201


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def err_404(e):
    return render_template_string(LAYOUT + """{% block content %}
    <h1>404 - Not Found</h1><p>That page doesn't exist.</p><a href="/">Home</a>
    {% endblock %}"""), 404

@app.errorhandler(403)
def err_403(e):
    return render_template_string(LAYOUT + """{% block content %}
    <h1>403 - Forbidden</h1><p>You don't have access to this.</p><a href="/">Home</a>
    {% endblock %}"""), 403


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            demo = User(username="demo", email="demo@example.com")
            demo.set_password("demo123")
            db.session.add(demo)
            db.session.commit()
            for title, url, tags in [
                ("Python Docs", "https://docs.python.org", "python, docs"),
                ("Flask Docs", "https://flask.palletsprojects.com", "flask, web, docs"),
                ("LangChain", "https://python.langchain.com", "ai, langchain"),
            ]:
                db.session.add(Bookmark(title=title, url=url, tags=tags, user_id=demo.id))
            db.session.commit()
            print("Seeded demo account (demo / demo123)")

    print("\n  Bookmark Manager running at http://127.0.0.1:5000")
    print("  Demo account: username=demo, password=demo123\n")
    app.run(debug=True, port=5000)


# =============================================================================
# WHAT YOU LEARNED IN THE FLASK COURSE
# =============================================================================
#
# Ch1:  Hello Flask - app, routes, running the server
# Ch2:  Routes - URL params, query params, GET/POST, redirects
# Ch3:  Templates - Jinja2, variables, loops, inheritance
# Ch4:  Forms - validation, flash messages, POST-Redirect-GET
# Ch5:  Databases - SQLAlchemy, models, CRUD operations
# Ch6:  REST APIs - JSON responses, HTTP methods, status codes
# Ch7:  Blueprints - project structure, modular routes
# Ch8:  Middleware - before/after request, error handlers, logging
# Ch9:  Authentication - sessions, password hashing, login_required
# Ch10: Full Project - all of the above combined
#
# =============================================================================
