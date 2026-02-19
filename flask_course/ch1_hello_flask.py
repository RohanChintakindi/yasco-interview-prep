"""
===========================================
 CHAPTER 1: HELLO FLASK - YOUR FIRST WEB APP
===========================================

WHAT IS FLASK?
--------------
Flask is a Python web framework. "Web framework" means it helps you
build websites and web APIs using Python.

When you visit a website like google.com, here's what happens:
  1. Your browser sends an HTTP REQUEST to Google's server
     ("Hey, I want the homepage")
  2. The server runs some code to figure out what to send back
  3. The server sends an HTTP RESPONSE back to your browser
     (the HTML/CSS/JS that makes up the page)

Flask is the code that runs in step 2. It:
  - Listens for incoming requests
  - Figures out which function to run based on the URL
  - Runs your Python code
  - Sends back a response

That's it. Flask is a very MINIMAL framework - it gives you the basics
and lets you add what you need. Compare that to Django, which is a
"batteries included" framework that gives you everything upfront.

Flask philosophy: "Give me the essentials, I'll add what I need."
Django philosophy: "Give me everything, I'll remove what I don't need."


WHY FLASK OVER DJANGO?
-----------------------
  Flask:
    - Lightweight, minimal, flexible
    - Great for APIs and microservices
    - Easy to learn (less magic, more explicit)
    - You choose your own database, auth, etc.
    - Popular for: APIs, small-medium apps, prototypes

  Django:
    - Full-featured, opinionated, batteries-included
    - Built-in admin panel, ORM, auth, forms
    - More structure enforced (MVC pattern)
    - Popular for: large apps, content sites, e-commerce


WHAT IS HTTP? (THE LANGUAGE OF THE WEB)
---------------------------------------
HTTP (HyperText Transfer Protocol) is how browsers talk to servers.

Every web interaction is a REQUEST -> RESPONSE cycle:

  Browser                           Server
    |                                 |
    |--- GET /about ----------------->|  (request: "give me the about page")
    |                                 |
    |<-- 200 OK, <html>...</html> ----|  (response: here's the HTML)
    |                                 |

HTTP METHODS (the "verbs" of the web):
  GET    = "Give me data"       (loading a page, fetching info)
  POST   = "Here's new data"    (submitting a form, creating something)
  PUT    = "Update this data"   (editing a profile, updating a record)
  DELETE = "Remove this data"   (deleting an account, removing a post)

STATUS CODES (the server's response):
  200 = OK (everything worked)
  201 = Created (new thing was made)
  301 = Moved Permanently (page moved to new URL)
  400 = Bad Request (you sent something wrong)
  404 = Not Found (that page doesn't exist)
  500 = Internal Server Error (the server broke)


INSTALL:
  pip install flask


HOW TO RUN THIS FILE:
  python ch1_hello_flask.py
  Then open http://127.0.0.1:5000 in your browser
"""

from flask import Flask


# =============================================================================
# CREATING THE APP
# =============================================================================
#
# Every Flask application starts by creating an "app" object.
# This object IS your web application. It handles:
#   - Routing (which URL goes to which function)
#   - Request handling (reading incoming data)
#   - Response generation (sending data back)
#   - Configuration (settings, secrets, etc.)
#
# __name__ tells Flask where your application is located.
# Flask uses this to find templates, static files, etc.
# Just always pass __name__ - it's the current module's name.

app = Flask(__name__)


# =============================================================================
# YOUR FIRST ROUTE
# =============================================================================
#
# A ROUTE is a mapping: URL -> Python function
#
# When someone visits http://127.0.0.1:5000/, Flask looks at its routes
# and says "oh, '/' is mapped to the index() function, let me run that."
#
# @app.route("/") is a DECORATOR. It says:
#   "Register the function below as the handler for this URL path."
#
# The function MUST return something - that's what gets sent back to the
# browser. It can be:
#   - A string (sent as HTML)
#   - A tuple (response, status_code)
#   - A Response object (for full control)
#   - JSON (for APIs)

@app.route("/")
def index():
    """This function runs when someone visits the homepage (/)."""
    return "<h1>Hello, Flask!</h1><p>Welcome to your first web app.</p>"

# That's it! You've mapped the URL "/" to a function that returns HTML.
# When someone visits http://127.0.0.1:5000/, they'll see "Hello, Flask!"


# =============================================================================
# MULTIPLE ROUTES
# =============================================================================
#
# You can have as many routes as you want. Each URL gets its own function.
# This is how websites have multiple pages: /about, /contact, /products, etc.

@app.route("/about")
def about():
    """Runs when someone visits /about."""
    return "<h1>About</h1><p>This is a Flask learning project.</p>"


@app.route("/contact")
def contact():
    """Runs when someone visits /contact."""
    return "<h1>Contact</h1><p>Email: hello@example.com</p>"


# Now you have 3 pages:
#   http://127.0.0.1:5000/        -> "Hello, Flask!"
#   http://127.0.0.1:5000/about   -> "About"
#   http://127.0.0.1:5000/contact -> "Contact"


# =============================================================================
# RETURNING HTML
# =============================================================================
#
# Returning raw HTML strings works, but it gets messy fast.
# In Chapter 3, we'll learn about TEMPLATES (separate HTML files).
# For now, raw strings are fine for learning.

@app.route("/styled")
def styled():
    """You can return any valid HTML."""
    return """
    <html>
    <head><title>Styled Page</title></head>
    <body style="font-family: Arial; max-width: 600px; margin: 50px auto;">
        <h1 style="color: #2c3e50;">Styled Page</h1>
        <p>This is a page with inline CSS styling.</p>
        <ul>
            <li>Flask is lightweight</li>
            <li>Flask is flexible</li>
            <li>Flask is fun to learn</li>
        </ul>
        <a href="/">Back to home</a>
    </body>
    </html>
    """


# =============================================================================
# RETURNING DIFFERENT STATUS CODES
# =============================================================================
#
# By default, Flask returns status code 200 (OK).
# You can return a different code by returning a tuple:
#   return (response_body, status_code)

@app.route("/teapot")
def teapot():
    """
    HTTP 418 "I'm a teapot" - a real status code from an April Fools RFC!
    """
    return "<h1>I'm a teapot</h1><p>I can't brew coffee.</p>", 418


# =============================================================================
# WHAT HAPPENS WHEN YOU VISIT A URL THAT DOESN'T EXIST?
# =============================================================================
#
# Try visiting http://127.0.0.1:5000/doesnt-exist
# You'll get a 404 Not Found error. Flask handles this automatically.
# In Chapter 9, we'll learn how to customize error pages.


# =============================================================================
# RUNNING THE APP
# =============================================================================
#
# app.run() starts Flask's built-in development server.
# It listens on http://127.0.0.1:5000 by default.
#
# 127.0.0.1 = "localhost" = your own computer
# 5000 = the port number
#
# PARAMETERS:
#   debug=True:
#     - Auto-restarts when you change code (HUGE time saver)
#     - Shows detailed error pages in the browser
#     - NEVER use debug=True in production (security risk)
#
#   port=5000:
#     - Which port to listen on. Change if 5000 is taken.
#
# The if __name__ == "__main__" check:
#   This makes sure the server only starts when you RUN this file
#   directly (python ch1.py), not when you IMPORT it from another file.

if __name__ == "__main__":
    print("=" * 50)
    print("  Starting Flask development server...")
    print("  Open http://127.0.0.1:5000 in your browser")
    print("  Press Ctrl+C to stop the server")
    print("=" * 50)

    app.run(debug=True, port=5000)


# =============================================================================
# TRY THESE AFTER RUNNING:
# =============================================================================
#
# 1. Open http://127.0.0.1:5000 in your browser
# 2. Try http://127.0.0.1:5000/about
# 3. Try http://127.0.0.1:5000/contact
# 4. Try http://127.0.0.1:5000/styled
# 5. Try http://127.0.0.1:5000/teapot
# 6. Try http://127.0.0.1:5000/nonexistent (404!)
#
# 7. While the server is running, edit the return string of index()
#    and save the file. Flask will auto-restart (debug=True) and
#    refresh the browser to see your changes!
#
#
# QUICK REFERENCE
# ===============
#
#   from flask import Flask
#   app = Flask(__name__)
#
#   @app.route("/path")
#   def function_name():
#       return "HTML or text"
#
#   app.run(debug=True)
#
# =============================================================================
