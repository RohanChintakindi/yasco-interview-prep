"""
=====================================================
 CHAPTER 8: MIDDLEWARE, ERROR HANDLING & LOGGING
=====================================================

WHAT IS MIDDLEWARE?
-------------------
Middleware is code that runs BEFORE or AFTER every request.
Flask calls them "hooks" - functions that fire at specific points
in the request lifecycle.

Use cases:
  - Log every request (who visited what, when)
  - Check authentication (is the user logged in?)
  - Add headers to every response (CORS, security)
  - Measure request timing (performance monitoring)
  - Handle errors gracefully (custom 404/500 pages)


THE REQUEST LIFECYCLE:
  1. Request comes in
  2. @app.before_request runs (middleware - before)
  3. The route function runs
  4. @app.after_request runs (middleware - after)
  5. Response goes out

  If an error occurs at step 3:
  3b. @app.errorhandler runs instead
  4.  @app.after_request still runs
  5.  Error response goes out


HOW TO RUN:
  python ch8_middleware_and_errors.py
"""

from flask import Flask, request, jsonify, g
import time
import logging

app = Flask(__name__)
app.secret_key = "dev-secret"


# =============================================================================
# PART 1: before_request - RUNS BEFORE EVERY REQUEST
# =============================================================================
#
# @app.before_request registers a function that runs BEFORE the route handler.
# If it returns something, that response is sent and the route is SKIPPED.
# If it returns None, the request continues to the route normally.

@app.before_request
def log_request_info():
    """Log every incoming request and start a timer."""
    g.start_time = time.time()  # g is a per-request storage object
    print(f"  -> {request.method} {request.path}")


@app.before_request
def check_maintenance_mode():
    """
    Example: block all requests during maintenance.
    Uncomment the return to enable "maintenance mode".
    """
    maintenance = False  # Set to True to enable
    if maintenance and request.path != "/health":
        return jsonify({"error": "Server is under maintenance"}), 503


# =============================================================================
# PART 2: after_request - RUNS AFTER EVERY REQUEST
# =============================================================================
#
# Receives the response object and MUST return it (possibly modified).
# Great for adding headers, logging response info, etc.

@app.after_request
def add_headers(response):
    """Add security and custom headers to every response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Powered-By"] = "Flask-Learning"

    # Log timing
    if hasattr(g, "start_time"):
        duration = time.time() - g.start_time
        response.headers["X-Response-Time"] = f"{duration:.4f}s"
        print(f"  <- {response.status_code} ({duration:.4f}s)")

    return response  # MUST return the response!


# =============================================================================
# PART 3: THE g OBJECT - PER-REQUEST STORAGE
# =============================================================================
#
# g (short for "global") is a special Flask object that:
#   - Exists for the duration of ONE request
#   - Is reset for each new request
#   - Is shared between before_request, the route, and after_request
#
# Use it to pass data between middleware and routes:
#   before_request: g.user = get_current_user()
#   route: print(g.user.name)
#   after_request: log(g.user)


# =============================================================================
# PART 4: CUSTOM ERROR HANDLERS
# =============================================================================
#
# By default, Flask shows ugly HTML error pages.
# You can customize them for a better user experience.

@app.errorhandler(404)
def handle_404(error):
    """Custom 404 page."""
    if request.path.startswith("/api/"):
        return jsonify({"error": "Endpoint not found", "path": request.path}), 404
    return """
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <a href="/">Go home</a>
    """, 404


@app.errorhandler(500)
def handle_500(error):
    """Custom 500 page."""
    return """
    <h1>500 - Server Error</h1>
    <p>Something went wrong on our end. Please try again later.</p>
    <a href="/">Go home</a>
    """, 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Catch-all for unhandled exceptions."""
    print(f"  !! Unhandled error: {error}")
    return jsonify({"error": "Internal server error", "detail": str(error)}), 500


# =============================================================================
# PART 5: ABORT - TRIGGERING ERRORS MANUALLY
# =============================================================================
#
# Use abort() to immediately stop and return an error response.

from flask import abort

@app.route("/api/secret")
def secret():
    """Example: check for an API key."""
    api_key = request.headers.get("X-API-Key")
    if api_key != "my-secret-key":
        abort(401)  # Triggers the 401 error handler
    return jsonify({"secret": "You found the secret!"})


@app.errorhandler(401)
def handle_401(error):
    return jsonify({"error": "Unauthorized. Provide a valid X-API-Key header."}), 401


# =============================================================================
# PART 6: LOGGING
# =============================================================================
#
# Python's built-in logging module is much better than print() for production.
# Levels: DEBUG < INFO < WARNING < ERROR < CRITICAL

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

@app.route("/log-demo")
def log_demo():
    logger.debug("This is a debug message (hidden by default)")
    logger.info("This is an info message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    return "<p>Check your terminal for log messages.</p><a href='/'>Home</a>"


# =============================================================================
# ROUTES
# =============================================================================

@app.route("/")
def index():
    return """
    <h1>Chapter 8: Middleware & Error Handling</h1>
    <p>Check your terminal - every request is being logged!</p>
    <ul>
        <li><a href="/">/</a> - This page</li>
        <li><a href="/health">/health</a> - Health check</li>
        <li><a href="/slow">/slow</a> - Slow endpoint (see timing header)</li>
        <li><a href="/oops">/oops</a> - Triggers a 500 error</li>
        <li><a href="/nonexistent">/nonexistent</a> - Triggers a 404</li>
        <li><a href="/api/secret">/api/secret</a> - Needs API key (401)</li>
        <li><a href="/log-demo">/log-demo</a> - Logging demo</li>
    </ul>
    <p><em>Check response headers (F12 -> Network tab) for X-Response-Time!</em></p>
    """


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/slow")
def slow():
    """Simulates a slow endpoint. Check X-Response-Time header!"""
    time.sleep(1)
    return "<p>This took ~1 second. Check the X-Response-Time header in DevTools!</p>"


@app.route("/oops")
def oops():
    """Deliberately raises an error to test error handling."""
    raise ValueError("Something went wrong on purpose!")


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# Before every request:
#   @app.before_request
#   def before(): ...
#
# After every request:
#   @app.after_request
#   def after(response): ... ; return response
#
# Error handlers:
#   @app.errorhandler(404)
#   def not_found(error): return "Not found", 404
#
# Trigger errors:
#   from flask import abort
#   abort(404)  # or 401, 403, 500, etc.
#
# Per-request storage:
#   g.my_data = "available in this request only"
#
# =============================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
