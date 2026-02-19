"""
=====================================================
 CHAPTER 4: FORMS & USER INPUT
=====================================================

WHAT WE'RE LEARNING
--------------------
Web apps need to COLLECT data from users: login forms, search bars,
settings pages, contact forms. This chapter covers:

  1. HTML forms with Flask (GET and POST)
  2. Reading form data safely
  3. Form validation (is the email valid? is the password long enough?)
  4. Flash messages (success/error notifications)
  5. Redirecting after form submission (POST-Redirect-GET pattern)


THE POST-REDIRECT-GET PATTERN
------------------------------
When a user submits a form:
  1. Browser sends POST request with form data
  2. Server processes it
  3. Server REDIRECTS to a GET page (don't return HTML directly from POST)

Why redirect? If you return HTML from POST and the user refreshes,
the browser resends the POST (double-submitting the form). Redirect avoids this.

  POST /register -> process data -> redirect to GET /success
  (refresh now just reloads /success, doesn't resubmit)


HOW TO RUN:
  python ch4_forms_and_validation.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)

# Secret key needed for flash messages and sessions
# In production, use a random secure key, not this!
app.secret_key = "dev-secret-key-change-in-production"


# =============================================================================
# SETUP: CREATE TEMPLATES
# =============================================================================

template_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(template_dir, exist_ok=True)

with open(os.path.join(template_dir, "form_base.html"), "w") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Forms{% endblock %}</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        form { background: #f9f9f9; padding: 20px; border-radius: 8px; }
        label { display: block; margin: 10px 0 5px; font-weight: bold; }
        input, textarea, select { width: 100%; padding: 8px; margin-bottom: 10px; box-sizing: border-box; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        .flash { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .flash.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .flash.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .error-text { color: red; font-size: 0.9em; }
        nav { margin-bottom: 20px; }
        nav a { margin-right: 15px; }
    </style>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/register">Register</a>
        <a href="/contact">Contact</a>
        <a href="/survey">Survey</a>
    </nav>

    {# Display flash messages #}
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
            <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
    {% endwith %}

    {% block content %}{% endblock %}
</body>
</html>
""")

with open(os.path.join(template_dir, "register.html"), "w") as f:
    f.write("""{% extends "form_base.html" %}
{% block title %}Register{% endblock %}
{% block content %}
<h1>Register</h1>
<form method="POST">
    <label>Username:</label>
    <input type="text" name="username" value="{{ values.username or '' }}" required>
    {% if errors.username %}<p class="error-text">{{ errors.username }}</p>{% endif %}

    <label>Email:</label>
    <input type="email" name="email" value="{{ values.email or '' }}" required>
    {% if errors.email %}<p class="error-text">{{ errors.email }}</p>{% endif %}

    <label>Password:</label>
    <input type="password" name="password" required>
    {% if errors.password %}<p class="error-text">{{ errors.password }}</p>{% endif %}

    <label>Confirm Password:</label>
    <input type="password" name="confirm_password" required>

    <button type="submit">Register</button>
</form>
{% endblock %}
""")

with open(os.path.join(template_dir, "contact.html"), "w") as f:
    f.write("""{% extends "form_base.html" %}
{% block title %}Contact{% endblock %}
{% block content %}
<h1>Contact Us</h1>
<form method="POST">
    <label>Name:</label>
    <input type="text" name="name" required>
    <label>Email:</label>
    <input type="email" name="email" required>
    <label>Subject:</label>
    <select name="subject">
        <option value="general">General Inquiry</option>
        <option value="support">Technical Support</option>
        <option value="feedback">Feedback</option>
    </select>
    <label>Message:</label>
    <textarea name="message" rows="5" required></textarea>
    <button type="submit">Send</button>
</form>
{% endblock %}
""")

with open(os.path.join(template_dir, "survey.html"), "w") as f:
    f.write("""{% extends "form_base.html" %}
{% block title %}Survey{% endblock %}
{% block content %}
<h1>Developer Survey</h1>
<form method="POST">
    <label>Favorite Language:</label>
    <select name="language">
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
        <option value="rust">Rust</option>
        <option value="go">Go</option>
    </select>

    <label>Experience Level:</label>
    <input type="radio" name="level" value="beginner"> Beginner
    <input type="radio" name="level" value="intermediate"> Intermediate
    <input type="radio" name="level" value="advanced"> Advanced

    <label>Interests (check all):</label>
    <input type="checkbox" name="interests" value="web"> Web Dev
    <input type="checkbox" name="interests" value="ai"> AI/ML
    <input type="checkbox" name="interests" value="mobile"> Mobile
    <input type="checkbox" name="interests" value="devops"> DevOps

    <br><br>
    <button type="submit">Submit</button>
</form>
{% endblock %}
""")

with open(os.path.join(template_dir, "form_home.html"), "w") as f:
    f.write("""{% extends "form_base.html" %}
{% block title %}Home{% endblock %}
{% block content %}
<h1>Chapter 4: Forms & Validation</h1>
<ul>
    <li><a href="/register">Registration Form</a> (with validation)</li>
    <li><a href="/contact">Contact Form</a> (with flash messages)</li>
    <li><a href="/survey">Survey</a> (radio buttons, checkboxes, select)</li>
</ul>
{% endblock %}
""")


# =============================================================================
# ROUTES
# =============================================================================

@app.route("/")
def home():
    return render_template("form_home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration form with manual validation.

    GET:  Show the empty form
    POST: Validate the data, show errors or redirect to success
    """
    errors = {}
    values = {}

    if request.method == "POST":
        # Read form data
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        values = {"username": username, "email": email}

        # VALIDATE
        if len(username) < 3:
            errors["username"] = "Username must be at least 3 characters"
        if "@" not in email or "." not in email:
            errors["email"] = "Please enter a valid email"
        if len(password) < 6:
            errors["password"] = "Password must be at least 6 characters"
        elif password != confirm:
            errors["password"] = "Passwords don't match"

        # If no errors, success!
        if not errors:
            flash(f"Account created for {username}!", "success")
            return redirect(url_for("home"))
            # POST-Redirect-GET pattern: redirect after successful POST

    # Show form (with errors if any)
    return render_template("register.html", errors=errors, values=values)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # In a real app, you'd send an email or save to database here
        flash(f"Thanks {name}! Your {subject} message has been received.", "success")
        return redirect(url_for("home"))

    return render_template("contact.html")


@app.route("/survey", methods=["GET", "POST"])
def survey():
    """
    Demonstrates different form input types:
    - select (dropdown)
    - radio buttons (single choice)
    - checkboxes (multiple choice)
    """
    if request.method == "POST":
        language = request.form.get("language")
        level = request.form.get("level", "not specified")
        # getlist() for checkboxes (multiple values with same name)
        interests = request.form.getlist("interests")

        flash(
            f"Survey received! Language: {language}, Level: {level}, "
            f"Interests: {', '.join(interests) or 'none'}",
            "success"
        )
        return redirect(url_for("home"))

    return render_template("survey.html")


# =============================================================================
# KEY CONCEPTS RECAP
# =============================================================================
#
# Reading form data:
#   request.form.get("field_name")        -> single value (str or None)
#   request.form.get("field", "default")  -> with default
#   request.form.getlist("checkboxes")    -> multiple values (list)
#
# Flash messages:
#   flash("message", "category")     -> set a message
#   get_flashed_messages()           -> read messages in template (one-time)
#   Categories: "success", "error", "info", "warning"
#
# POST-Redirect-GET:
#   1. POST /register (process form)
#   2. flash("Success!")
#   3. return redirect(url_for("home"))
#   4. GET /home (shows flash message)
#
# Validation:
#   Build an errors dict. If empty, success. If not, re-render form with errors.
#   Pass values back so the user doesn't have to retype everything.
#
# =============================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
