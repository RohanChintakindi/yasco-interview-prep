"""
=====================================================
 CHAPTER 2: ROUTES, URL PARAMETERS & HTTP METHODS
=====================================================

In Chapter 1, we made static routes: /about always shows the same page.
But real apps need DYNAMIC routes:
  /user/chint    -> shows Chint's profile
  /user/alice    -> shows Alice's profile
  /product/42    -> shows product #42

The URL itself carries information. Flask lets you capture parts of the
URL and pass them to your function as arguments.

We'll also learn about HTTP methods (GET vs POST) which are essential
for forms and APIs.


HOW TO RUN:
  python ch2_routes_and_urls.py
  Then open http://127.0.0.1:5000 in your browser
"""

from flask import Flask, request, redirect, url_for

app = Flask(__name__)


# =============================================================================
# PART 1: DYNAMIC URL PARAMETERS
# =============================================================================
#
# Use <variable_name> in the route to capture part of the URL.
# Flask passes it as an argument to your function.
#
# /user/<username> matches:
#   /user/chint   -> username = "chint"
#   /user/alice   -> username = "alice"
#   /user/bob123  -> username = "bob123"

@app.route("/")
def index():
    return """
    <h1>Chapter 2: Routes & URLs</h1>
    <ul>
        <li><a href="/user/chint">User: chint</a></li>
        <li><a href="/user/alice">User: alice</a></li>
        <li><a href="/product/42">Product: 42</a></li>
        <li><a href="/product/100">Product: 100</a></li>
        <li><a href="/greet/Chint/25">Greet with age</a></li>
        <li><a href="/search?q=flask&page=1">Search example</a></li>
        <li><a href="/form">Form example (POST)</a></li>
    </ul>
    """


@app.route("/user/<username>")
def user_profile(username):
    """
    <username> captures that part of the URL and passes it as a string.

    /user/chint -> username = "chint"
    /user/alice -> username = "alice"
    """
    return f"<h1>Profile: {username}</h1><p>Welcome to {username}'s page!</p>"


# =============================================================================
# PART 2: TYPE CONVERTERS
# =============================================================================
#
# By default, URL parameters are strings. But you can specify types:
#
#   <int:id>     -> converts to integer (rejects non-numbers)
#   <float:price> -> converts to float
#   <path:subpath> -> like string but allows slashes
#
# If the type doesn't match, Flask returns 404 automatically.
# /product/abc would return 404 because "abc" isn't an int.

@app.route("/product/<int:product_id>")
def product(product_id):
    """
    <int:product_id> only matches integers.

    /product/42  -> product_id = 42 (integer, not string!)
    /product/abc -> 404 Not Found (abc isn't an int)
    """
    return f"<h1>Product #{product_id}</h1><p>This is product number {product_id}.</p>"


# =============================================================================
# PART 3: MULTIPLE URL PARAMETERS
# =============================================================================
#
# You can have multiple parameters in one route.

@app.route("/greet/<name>/<int:age>")
def greet(name, age):
    """
    /greet/Chint/25 -> name = "Chint", age = 25
    """
    return f"<h1>Hello, {name}!</h1><p>You are {age} years old.</p>"


# =============================================================================
# PART 4: QUERY PARAMETERS
# =============================================================================
#
# URL parameters (/user/<name>) are part of the URL PATH.
# Query parameters (?key=value) are AFTER the ? in the URL.
#
# Example: /search?q=flask&page=2
#   Path: /search
#   Query params: q = "flask", page = "2"
#
# You access query params with request.args (it's like a dict).
#
# WHEN TO USE WHICH:
#   URL params:   for identifying a RESOURCE (/user/chint, /product/42)
#   Query params: for FILTERING or OPTIONS (/search?q=flask&sort=date)

@app.route("/search")
def search():
    """
    /search?q=flask&page=1
    request.args["q"]    -> "flask"
    request.args["page"] -> "1" (always a string!)
    """
    # request.args is a dict-like object with query parameters
    # .get() returns None if the key doesn't exist (avoids errors)
    query = request.args.get("q", "")         # default to empty string
    page = request.args.get("page", "1")      # default to "1"

    return f"""
    <h1>Search Results</h1>
    <p>You searched for: <strong>{query}</strong></p>
    <p>Page: {page}</p>
    <p><em>request.args = {dict(request.args)}</em></p>
    <br>
    <p>Try: <a href="/search?q=python&page=2&sort=date">/search?q=python&page=2&sort=date</a></p>
    """


# =============================================================================
# PART 5: HTTP METHODS - GET vs POST
# =============================================================================
#
# So far, all our routes handle GET requests (loading a page).
# But forms SUBMIT data with POST requests.
#
# GET:  "Give me something" (browser loading a page)
# POST: "Here, take this data" (form submission, creating something)
#
# By default, @app.route only allows GET.
# To allow POST: @app.route("/path", methods=["GET", "POST"])
#
# HOW TO TELL WHICH METHOD WAS USED: request.method

@app.route("/form", methods=["GET", "POST"])
def form_example():
    """
    GET  /form -> Show the form
    POST /form -> Process the submitted form data
    """
    if request.method == "GET":
        # User is visiting the page -> show the form
        return """
        <h1>Contact Form</h1>
        <form method="POST" action="/form">
            <label>Name: <input type="text" name="name"></label><br><br>
            <label>Email: <input type="email" name="email"></label><br><br>
            <label>Message:<br>
                <textarea name="message" rows="4" cols="40"></textarea>
            </label><br><br>
            <button type="submit">Send</button>
        </form>
        """
    else:
        # User submitted the form -> process the data
        # Form data is in request.form (for POST requests)
        name = request.form.get("name", "Unknown")
        email = request.form.get("email", "Unknown")
        message = request.form.get("message", "")

        return f"""
        <h1>Form Submitted!</h1>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Message:</strong> {message}</p>
        <br>
        <a href="/form">Submit another</a>
        """

# IMPORTANT: request.args = query params (GET data, from the URL)
#            request.form = form data (POST data, from the form body)
#            request.json = JSON data (from API requests with JSON body)


# =============================================================================
# PART 6: REDIRECTS
# =============================================================================
#
# Sometimes you want to send the user to a DIFFERENT page.
# redirect() sends an HTTP 302 (redirect) response.
#
# url_for() generates a URL from a function name.
# Why not just hardcode "/user/chint"? Because if you later rename
# the route, url_for() still works. It's the safe way.

@app.route("/go-home")
def go_home():
    """Redirects the user to the index page."""
    return redirect(url_for("index"))
    # url_for("index") generates "/" (the URL for the index function)


@app.route("/go-to-user/<username>")
def go_to_user(username):
    """Redirects to a user's profile."""
    return redirect(url_for("user_profile", username=username))
    # url_for("user_profile", username="chint") generates "/user/chint"


# =============================================================================
# PART 7: THE request OBJECT
# =============================================================================
#
# `request` is a special Flask object that holds ALL information about
# the current HTTP request. It's available in any route function.
#
# Most useful attributes:
#   request.method      -> "GET", "POST", "PUT", "DELETE"
#   request.args        -> query parameters (?key=value)
#   request.form        -> form data (from POST forms)
#   request.json        -> JSON body (from API requests)
#   request.headers     -> HTTP headers (User-Agent, Content-Type, etc.)
#   request.url         -> the full URL
#   request.path        -> just the path part (/about)
#   request.remote_addr -> the client's IP address

@app.route("/debug")
def debug_request():
    """Shows all the info available in the request object."""
    return f"""
    <h1>Request Debug Info</h1>
    <pre>
Method:      {request.method}
URL:         {request.url}
Path:        {request.path}
IP:          {request.remote_addr}
User-Agent:  {request.headers.get("User-Agent")}
Args:        {dict(request.args)}
    </pre>
    <p>Try: <a href="/debug?foo=bar&hello=world">/debug?foo=bar&hello=world</a></p>
    """


# =============================================================================
# PART 8: MULTIPLE ROUTES FOR ONE FUNCTION
# =============================================================================
#
# A function can have multiple route decorators.
# This is useful for aliases or default values.

@app.route("/hi")
@app.route("/hello")
@app.route("/hey")
def multi_greeting():
    """All three URLs lead to this same function."""
    return "<h1>Hey there!</h1><p>This page has 3 URLs: /hi, /hello, /hey</p>"


# =============================================================================
# RUN THE APP
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  Chapter 2: Routes & URLs")
    print("  Open http://127.0.0.1:5000")
    print("=" * 50)

    app.run(debug=True, port=5000)


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Dynamic URL parameter:
#   @app.route("/user/<username>")
#   def user(username):  # username is a string
#
# Typed parameter:
#   @app.route("/product/<int:id>")
#   def product(id):     # id is an integer
#
# Query parameters:
#   /search?q=flask -> request.args.get("q") -> "flask"
#
# HTTP methods:
#   @app.route("/form", methods=["GET", "POST"])
#   if request.method == "POST":
#       data = request.form.get("field_name")
#
# Redirect:
#   return redirect(url_for("function_name", param=value))
#
# =============================================================================
