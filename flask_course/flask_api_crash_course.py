"""
=====================================================
 FLASK API CRASH COURSE — Quick Revision
=====================================================

Everything you need for Flask REST APIs in one file.
No HTML, no templates, no Jinja — just JSON APIs.

INSTALL:
  pip install flask flask-sqlalchemy pyjwt

RUN:
  python flask_api_crash_course.py

TEST:
  Use the curl commands in the comments, or open browser to http://127.0.0.1:5000
"""

from flask import Flask, jsonify, request
from functools import wraps
import jwt
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"


# =============================================================================
# 1. BASICS — Routes & JSON responses
# =============================================================================
#
# @app.route(path)     — register a URL
# jsonify(data)        — return JSON (sets Content-Type header)
# return data, status  — set HTTP status code

@app.route("/")
def home():
    return jsonify({"message": "API is running"})


# URL parameters: <type:name>
@app.route("/api/users/<int:user_id>")
def get_user(user_id):
    return jsonify({"user_id": user_id, "name": f"User {user_id}"})


# Query parameters: /api/search?q=python&page=1
@app.route("/api/search")
def search():
    query = request.args.get("q", "")          # default ""
    page = request.args.get("page", 1, type=int)  # default 1, cast to int
    return jsonify({"query": query, "page": page})


# =============================================================================
# 2. HTTP METHODS — GET, POST, PUT, DELETE
# =============================================================================
#
# GET    = read data           (no body)
# POST   = create something    (send JSON body)
# PUT    = update something    (send JSON body)
# DELETE = delete something    (no body)
#
# request.get_json()  — parse the JSON body from POST/PUT
# request.method      — which HTTP method was used
# request.headers     — access request headers
#
# STATUS CODES:
#   200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error

# In-memory "database" for demo
BOOKS = [
    {"id": 1, "title": "Dune", "author": "Frank Herbert"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "Neuromancer", "author": "William Gibson"},
]
next_id = 4


# GET all
@app.route("/api/books", methods=["GET"])
def list_books():
    # Filtering: /api/books?author=orwell
    author = request.args.get("author")
    if author:
        filtered = [b for b in BOOKS if author.lower() in b["author"].lower()]
        return jsonify(filtered)
    return jsonify(BOOKS)


# GET one
@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


# POST — create
# curl -X POST http://127.0.0.1:5000/api/books -H "Content-Type: application/json" -d '{"title":"Snow Crash","author":"Neal Stephenson"}'
@app.route("/api/books", methods=["POST"])
def create_book():
    global next_id
    data = request.get_json()

    # Validation
    if not data or not data.get("title") or not data.get("author"):
        return jsonify({"error": "title and author are required"}), 400

    book = {"id": next_id, "title": data["title"], "author": data["author"]}
    next_id += 1
    BOOKS.append(book)
    return jsonify(book), 201  # 201 = Created


# PUT — update
# curl -X PUT http://127.0.0.1:5000/api/books/1 -H "Content-Type: application/json" -d '{"title":"Dune Messiah"}'
@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    return jsonify(book)


# DELETE
# curl -X DELETE http://127.0.0.1:5000/api/books/1
@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global BOOKS
    before = len(BOOKS)
    BOOKS = [b for b in BOOKS if b["id"] != book_id]
    if len(BOOKS) == before:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"message": "Deleted"}), 200


# =============================================================================
# 3. BLUEPRINTS — Splitting your API into modules
# =============================================================================
#
# In a real project you'd split routes into separate files:
#
#   myapi/
#     app.py
#     blueprints/
#       users.py    <- Blueprint("users", __name__)
#       books.py    <- Blueprint("books", __name__)
#
# In users.py:
#   from flask import Blueprint, jsonify
#   users_bp = Blueprint("users", __name__)
#
#   @users_bp.route("/")
#   def list_users():
#       return jsonify([...])
#
# In app.py:
#   from blueprints.users import users_bp
#   app.register_blueprint(users_bp, url_prefix="/api/users")
#
# Now /api/users/ hits the users blueprint.
# Each team member can work on their own blueprint file.


# =============================================================================
# 4. DATABASE — Flask-SQLAlchemy
# =============================================================================
#
# SETUP (uncomment to use):
#
#   from flask_sqlalchemy import SQLAlchemy
#   app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
#   db = SQLAlchemy(app)
#
# DEFINE A MODEL:
#
#   class User(db.Model):
#       id = db.Column(db.Integer, primary_key=True)
#       name = db.Column(db.String(100), nullable=False)
#       email = db.Column(db.String(120), unique=True, nullable=False)
#
#       def to_dict(self):
#           return {"id": self.id, "name": self.name, "email": self.email}
#
# CREATE TABLES:
#
#   with app.app_context():
#       db.create_all()
#
# CRUD OPERATIONS:
#
#   # Create
#   user = User(name="Chint", email="chint@example.com")
#   db.session.add(user)
#   db.session.commit()
#
#   # Read
#   users = User.query.all()                    # all users
#   user = User.query.get(1)                    # by id
#   user = User.query.filter_by(name="Chint").first()  # by field
#
#   # Update
#   user.name = "New Name"
#   db.session.commit()
#
#   # Delete
#   db.session.delete(user)
#   db.session.commit()
#
# RELATIONSHIPS (one-to-many):
#
#   class User(db.Model):
#       id = db.Column(db.Integer, primary_key=True)
#       name = db.Column(db.String(100))
#       posts = db.relationship("Post", backref="author")
#
#   class Post(db.Model):
#       id = db.Column(db.Integer, primary_key=True)
#       title = db.Column(db.String(200))
#       user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#
#   # Now: user.posts gives all posts, post.author gives the user


# =============================================================================
# 5. AUTHENTICATION — JWT Tokens
# =============================================================================
#
# Flow:
#   1. User POSTs username/password to /api/login
#   2. Server creates a JWT token and returns it
#   3. User sends token in header: Authorization: Bearer <token>
#   4. Server verifies token on protected routes

USERS_DB = {
    "chint": "password123",  # In real apps: hash with werkzeug!
}


# Login — returns a JWT token
# curl -X POST http://127.0.0.1:5000/api/login -H "Content-Type: application/json" -d '{"username":"chint","password":"password123"}'
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    if USERS_DB.get(username) != password:
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token
    token = jwt.encode(
        {
            "user": username,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify({"token": token})


# Decorator to protect routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token missing"}), 401
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.current_user = payload["user"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


# Protected route — needs valid token
# curl http://127.0.0.1:5000/api/profile -H "Authorization: Bearer YOUR_TOKEN_HERE"
@app.route("/api/profile")
@token_required
def profile():
    return jsonify({"user": request.current_user, "message": "You're authenticated!"})


# =============================================================================
# 6. ERROR HANDLING & MIDDLEWARE
# =============================================================================

# Custom error handlers — return JSON, not HTML
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# Before every request — runs first (logging, auth checks, etc.)
@app.before_request
def log_request():
    print(f"  -> {request.method} {request.path}")


# After every request — runs last (add headers like CORS)
@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
    return response


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Route:          @app.route("/path", methods=["GET", "POST"])
# URL param:      /users/<int:id>  ->  def get_user(id)
# Query param:    request.args.get("key", default)
# JSON body:      request.get_json()
# Return JSON:    return jsonify(data), status_code
#
# Status codes:   200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found
#
# SQLAlchemy:     db.session.add(obj), .commit(), .delete(obj)
#                 Model.query.all(), .get(id), .filter_by(field=val).first()
#
# JWT:            jwt.encode(payload, secret), jwt.decode(token, secret)
#                 Authorization: Bearer <token>
#
# Middleware:      @app.before_request, @app.after_request
# Error handler:  @app.errorhandler(404)
# Blueprint:      bp = Blueprint("name", __name__); app.register_blueprint(bp, url_prefix="/api")
#
# =============================================================================


if __name__ == "__main__":
    print("\n  Flask API Crash Course")
    print("  Test these endpoints:")
    print("    GET  http://127.0.0.1:5000/")
    print("    GET  http://127.0.0.1:5000/api/books")
    print("    GET  http://127.0.0.1:5000/api/books/1")
    print("    POST http://127.0.0.1:5000/api/books  (JSON body)")
    print("    POST http://127.0.0.1:5000/api/login   (JSON body)")
    print("    GET  http://127.0.0.1:5000/api/profile  (needs token)\n")
    app.run(debug=True)
