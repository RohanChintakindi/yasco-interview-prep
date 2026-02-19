"""
=====================================================
 CHAPTER 6: REST APIs & JSON
=====================================================

WHAT IS A REST API?
-------------------
So far we've returned HTML pages. But what if your client is:
  - A React/Vue frontend (not Jinja templates)
  - A mobile app (iOS/Android)
  - Another server (microservices)
  - A Python script

They don't want HTML. They want raw DATA. Usually JSON.

A REST API returns JSON instead of HTML:

  HTML response: <h1>Chint</h1><p>chint@example.com</p>
  JSON response: {"name": "Chint", "email": "chint@example.com"}

REST (Representational State Transfer) is a CONVENTION for how APIs
should be structured. It uses HTTP methods as verbs:

  GET    /api/users          -> List all users
  GET    /api/users/1        -> Get user #1
  POST   /api/users          -> Create a new user
  PUT    /api/users/1        -> Update user #1
  DELETE /api/users/1        -> Delete user #1

The URL is the NOUN (what resource), the HTTP method is the VERB (what action).


HOW TO RUN:
  python ch6_rest_api.py

TEST WITH:
  curl http://127.0.0.1:5000/api/users
  Or use the built-in test page at http://127.0.0.1:5000
"""

from flask import Flask, jsonify, request
import os

app = Flask(__name__)


# =============================================================================
# FAKE DATABASE (in-memory for simplicity)
# =============================================================================

users_db = [
    {"id": 1, "name": "Chint", "email": "chint@example.com", "role": "admin"},
    {"id": 2, "name": "Alice", "email": "alice@example.com", "role": "user"},
    {"id": 3, "name": "Bob", "email": "bob@example.com", "role": "user"},
]
next_id = 4


# =============================================================================
# PART 1: jsonify() - RETURNING JSON
# =============================================================================
#
# jsonify() converts a Python dict/list into a JSON HTTP response.
# It also sets the Content-Type header to "application/json".
#
# return {"name": "Chint"}     -> Flask auto-converts dicts to JSON (Flask 2.2+)
# return jsonify({"name": "Chint"})  -> Explicit, works in all versions

# --- GET all users ---
@app.route("/api/users", methods=["GET"])
def get_users():
    """
    GET /api/users -> Returns list of all users as JSON

    Optional query params for filtering:
      /api/users?role=admin
    """
    role = request.args.get("role")

    if role:
        filtered = [u for u in users_db if u["role"] == role]
        return jsonify(filtered)

    return jsonify(users_db)


# --- GET one user ---
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """GET /api/users/1 -> Returns one user or 404"""
    user = next((u for u in users_db if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404
        # Note: returning a TUPLE (json, status_code) to set 404

    return jsonify(user)


# =============================================================================
# PART 2: HANDLING JSON INPUT (POST/PUT)
# =============================================================================
#
# When a client sends data to your API, it comes as JSON in the request body.
# Access it with request.json (or request.get_json()).
#
# The client must set Content-Type: application/json in their request headers.

# --- CREATE a user ---
@app.route("/api/users", methods=["POST"])
def create_user():
    """
    POST /api/users
    Body: {"name": "Eve", "email": "eve@example.com", "role": "user"}
    -> Creates and returns the new user with 201 status
    """
    global next_id

    data = request.json  # Parse the JSON body

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Validate required fields
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    new_user = {
        "id": next_id,
        "name": data["name"],
        "email": data["email"],
        "role": data.get("role", "user"),  # Default to "user"
    }
    users_db.append(new_user)
    next_id += 1

    return jsonify(new_user), 201  # 201 = Created


# --- UPDATE a user ---
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    PUT /api/users/1
    Body: {"name": "Chint Updated", "email": "new@example.com"}
    -> Updates and returns the user
    """
    user = next((u for u in users_db if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Update only the fields that were provided
    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]
    if "role" in data:
        user["role"] = data["role"]

    return jsonify(user)


# --- DELETE a user ---
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    DELETE /api/users/1
    -> Deletes the user, returns confirmation
    """
    global users_db
    user = next((u for u in users_db if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    users_db = [u for u in users_db if u["id"] != user_id]
    return jsonify({"message": f"User {user_id} deleted"})


# =============================================================================
# PART 3: ERROR HANDLING FOR APIs
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    """Return JSON instead of HTML for 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


# =============================================================================
# TEST PAGE (HTML page to test the API from browser)
# =============================================================================

@app.route("/")
def test_page():
    return """
    <html><head><title>API Tester</title>
    <style>body{font-family:monospace;max-width:800px;margin:40px auto;padding:0 20px}
    button{margin:5px;padding:8px 15px;cursor:pointer}
    pre{background:#f4f4f4;padding:15px;border-radius:5px;overflow:auto}
    </style></head><body>
    <h1>REST API Tester</h1>
    <p>Click buttons to test API endpoints:</p>
    <button onclick="test('GET', '/api/users')">GET all users</button>
    <button onclick="test('GET', '/api/users/1')">GET user 1</button>
    <button onclick="test('GET', '/api/users?role=admin')">GET admins</button>
    <button onclick="test('POST', '/api/users', {name:'Eve',email:'eve@test.com',role:'user'})">POST new user</button>
    <button onclick="test('PUT', '/api/users/1', {name:'Chint Updated'})">PUT update user 1</button>
    <button onclick="test('DELETE', '/api/users/3')">DELETE user 3</button>
    <button onclick="test('GET', '/api/users/999')">GET user 999 (404)</button>
    <h3>Response:</h3>
    <pre id="output">Click a button above...</pre>
    <script>
    async function test(method, url, body) {
        const opts = {method, headers: {'Content-Type': 'application/json'}};
        if (body) opts.body = JSON.stringify(body);
        const res = await fetch(url, opts);
        const data = await res.json();
        document.getElementById('output').textContent =
            method + ' ' + url + '\\nStatus: ' + res.status + '\\n\\n' + JSON.stringify(data, null, 2);
    }
    </script></body></html>
    """


# =============================================================================
# REST API CHEAT SHEET
# =============================================================================
#
# Return JSON:
#   return jsonify(data)              -> 200 OK
#   return jsonify(data), 201         -> 201 Created
#   return jsonify({"error": ""}), 404 -> 404 Not Found
#
# Read JSON input:
#   data = request.json               -> dict from request body
#
# Read query params:
#   value = request.args.get("key")   -> from ?key=value in URL
#
# HTTP methods:
#   GET    -> Read (list or detail)
#   POST   -> Create
#   PUT    -> Update (full replace)
#   PATCH  -> Update (partial)
#   DELETE -> Delete
#
# Status codes:
#   200 OK, 201 Created, 204 No Content
#   400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
#   500 Internal Server Error
#
# =============================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
