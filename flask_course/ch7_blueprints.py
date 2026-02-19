"""
=====================================================
 CHAPTER 7: BLUEPRINTS & PROJECT STRUCTURE
=====================================================

THE PROBLEM
-----------
So far, everything is in ONE file. That works for learning, but real
apps have dozens of routes. One 2000-line file is unmaintainable.

BLUEPRINTS let you split your app into modules:
  - auth.py    -> login, register, logout routes
  - api.py     -> REST API routes
  - main.py    -> homepage, about, etc.

Each module is a Blueprint - a mini Flask app that gets registered
with the main app.

Think of it like departments in a company:
  Company (Flask app)
    ├── Sales Department (auth blueprint)
    ├── Engineering Department (api blueprint)
    └── HR Department (main blueprint)

Each department operates independently but is part of the same company.


REAL PROJECT STRUCTURE:
  my_app/
  ├── app.py              <- Creates the Flask app
  ├── config.py           <- Settings
  ├── models.py           <- Database models
  ├── blueprints/
  │   ├── __init__.py
  │   ├── main.py         <- Homepage, about, etc.
  │   ├── auth.py         <- Login, register, logout
  │   └── api.py          <- REST API endpoints
  ├── templates/
  │   ├── base.html
  │   ├── main/
  │   │   └── index.html
  │   └── auth/
  │       └── login.html
  └── static/
      ├── css/
      └── js/


For this chapter, we'll keep it in one file but show the Blueprint pattern.


HOW TO RUN:
  python ch7_blueprints.py
"""

from flask import Flask, Blueprint, jsonify, render_template_string

# =============================================================================
# PART 1: CREATING BLUEPRINTS
# =============================================================================
#
# Blueprint(name, import_name, url_prefix)
#   name:       A unique name for this blueprint
#   import_name: Usually __name__
#   url_prefix:  All routes in this blueprint start with this prefix
#
# url_prefix="/api" means:
#   @api_bp.route("/users")  ->  /api/users (prefix is prepended)

# --- Main Blueprint (public pages) ---
main_bp = Blueprint("main", __name__, url_prefix="")

@main_bp.route("/")
def index():
    return """
    <h1>Chapter 7: Blueprints</h1>
    <ul>
        <li><a href="/">/</a> - This page (main blueprint)</li>
        <li><a href="/about">/about</a> - About (main blueprint)</li>
        <li><a href="/auth/login">/auth/login</a> - Login (auth blueprint)</li>
        <li><a href="/auth/register">/auth/register</a> - Register (auth blueprint)</li>
        <li><a href="/api/v1/status">/api/v1/status</a> - API status (api blueprint)</li>
        <li><a href="/api/v1/users">/api/v1/users</a> - API users (api blueprint)</li>
        <li><a href="/admin/dashboard">/admin/dashboard</a> - Admin (admin blueprint)</li>
    </ul>
    """

@main_bp.route("/about")
def about():
    return "<h1>About</h1><p>This app demonstrates Flask Blueprints.</p><a href='/'>Home</a>"


# --- Auth Blueprint (authentication routes) ---
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login")
def login():
    return "<h1>Login Page</h1><p>This is from the auth blueprint (/auth/login)</p><a href='/'>Home</a>"

@auth_bp.route("/register")
def register():
    return "<h1>Register Page</h1><p>This is from the auth blueprint (/auth/register)</p><a href='/'>Home</a>"

@auth_bp.route("/logout")
def logout():
    return "<h1>Logged Out</h1><a href='/'>Home</a>"


# --- API Blueprint (JSON endpoints) ---
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

@api_bp.route("/status")
def api_status():
    return jsonify({"status": "ok", "version": "1.0", "blueprint": "api"})

@api_bp.route("/users")
def api_users():
    return jsonify([
        {"id": 1, "name": "Chint"},
        {"id": 2, "name": "Alice"},
    ])


# --- Admin Blueprint ---
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
def dashboard():
    return "<h1>Admin Dashboard</h1><p>This is from the admin blueprint (/admin/dashboard)</p><a href='/'>Home</a>"


# =============================================================================
# PART 2: REGISTERING BLUEPRINTS WITH THE APP
# =============================================================================
#
# Blueprints don't do anything until you REGISTER them with the Flask app.
# app.register_blueprint() connects the blueprint to the app.

app = Flask(__name__)

app.register_blueprint(main_bp)    # Routes: /, /about
app.register_blueprint(auth_bp)    # Routes: /auth/login, /auth/register, /auth/logout
app.register_blueprint(api_bp)     # Routes: /api/v1/status, /api/v1/users
app.register_blueprint(admin_bp)   # Routes: /admin/dashboard


# =============================================================================
# PART 3: BLUEPRINT-SPECIFIC ERROR HANDLERS
# =============================================================================

@api_bp.errorhandler(404)
def api_not_found(error):
    """API routes return JSON errors, not HTML."""
    return jsonify({"error": "API endpoint not found"}), 404


# =============================================================================
# PART 4: HOW TO STRUCTURE A REAL PROJECT
# =============================================================================
#
# In a real app, each blueprint would be in its own FILE:
#
# blueprints/main.py:
#   from flask import Blueprint
#   main_bp = Blueprint("main", __name__)
#
#   @main_bp.route("/")
#   def index():
#       return render_template("main/index.html")
#
#
# blueprints/auth.py:
#   from flask import Blueprint
#   auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
#
#   @auth_bp.route("/login")
#   def login(): ...
#
#
# app.py:
#   from flask import Flask
#   from blueprints.main import main_bp
#   from blueprints.auth import auth_bp
#   from blueprints.api import api_bp
#
#   def create_app():
#       app = Flask(__name__)
#       app.register_blueprint(main_bp)
#       app.register_blueprint(auth_bp)
#       app.register_blueprint(api_bp)
#       return app
#
# The create_app() pattern is called the APPLICATION FACTORY.
# It's the recommended way to structure Flask apps because:
#   1. You can create multiple app instances (for testing)
#   2. Configuration can vary per instance
#   3. Avoids circular imports


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Create a blueprint:
#   bp = Blueprint("name", __name__, url_prefix="/prefix")
#
# Add routes to blueprint:
#   @bp.route("/path")
#   def handler(): ...
#
# Register with app:
#   app.register_blueprint(bp)
#
# URL building across blueprints:
#   url_for("main.index")       -> /
#   url_for("auth.login")       -> /auth/login
#   url_for("api.api_users")    -> /api/v1/users
#
# =============================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
