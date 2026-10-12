from functools import wraps

import bcrypt
from flask import redirect, session


def hash_password(password):
    # bcrypt only reads the first 72 bytes
    return bcrypt.hashpw(password.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def check_password(password, stored_hash):
    try:
        return bcrypt.checkpw(password.encode("utf-8")[:72], stored_hash.encode("utf-8"))
    except ValueError:
        return False


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return view(*args, **kwargs)
    return wrapper


# ---- server-side validation: same rules and messages as the JavaScript ----

def validate_register(form):
    errors = {}
    name = form.get("name", "").strip()
    email = form.get("email", "").strip()
    password = form.get("password", "")
    confirm = form.get("confirm_password", "")

    if not name:
        errors["name"] = "Name is required"
    if not email:
        errors["email"] = "Email is required"
    if not password:
        errors["password"] = "Password is required"
    if not confirm:
        errors["confirm_password"] = "Confirm password is required"
    elif password and password != confirm:
        errors["confirm_password"] = "Passwords do not match"
    return errors


def validate_login(form):
    errors = {}
    if not form.get("email", "").strip():
        errors["email"] = "Email is required"
    if not form.get("password", ""):
        errors["password"] = "Password is required"
    return errors


def validate_title(title):
    title = title.strip()
    if not title:
        return "Title is required"
    if len(title) > 200:
        return "Title is too long (200 characters at most)"
    return ""
