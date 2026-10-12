import os

import pymysql
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session

import db
from auth_utils import (check_password, hash_password, login_required,
                        validate_login, validate_register, validate_title)

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET", "dev-only-change-me")


# ---------- helpers ----------

def render_todos(**extra):
    """Show the logged-in user's list, newest first. user_id comes from the session."""
    todos = db.fetch_all(
        "SELECT todo_id, title, is_done, created_at FROM todos "
        "WHERE user_id = %s ORDER BY todo_id DESC",
        (session["user_id"],),
    )
    return render_template("todos.html", todos=todos, **extra)


def log_in(user_id, name):
    session.clear()
    session["user_id"] = user_id
    session["name"] = name


# ---------- auth ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", errors={}, values={})

    errors = validate_register(request.form)
    values = {"name": request.form.get("name", ""), "email": request.form.get("email", "")}
    if errors:                                    # R8: show the page again, do not touch the database
        return render_template("register.html", errors=errors, values=values)

    name = request.form["name"].strip()
    email = request.form["email"].strip()
    try:
        _, new_id = db.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
            (email, name, hash_password(request.form["password"])),
        )
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:                     # duplicate entry for UNIQUE (email)
            return render_template("register.html", errors={"email": "Email Already Exists"}, values=values)
        raise

    log_in(new_id, name)
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
            return redirect("/")
        return render_template("login.html", errors={}, values={})

    errors = validate_login(request.form)
    values = {"email": request.form.get("email", "")}
    if errors:
        return render_template("login.html", errors=errors, values=values)

    user = db.fetch_one(
        "SELECT user_id, name, password_hash FROM users WHERE email = %s",
        (request.form["email"].strip(),),
    )
    # same message for an unknown e-mail and a wrong password
    if user is None or not check_password(request.form["password"], user["password_hash"]):
        return render_template("login.html", errors={"form": "Invalid email or password"}, values=values)

    log_in(user["user_id"], user["name"])
    return redirect("/")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/login")


# ---------- to-dos ----------

@app.route("/")
@login_required
def index():
    return render_todos()


@app.route("/todos/add", methods=["POST"])
@login_required
def add_todo():
    title = request.form.get("title", "")
    error = validate_title(title)
    if error:
        return render_todos(add_error=error, add_value=title)
    db.execute("INSERT INTO todos (user_id, title) VALUES (%s, %s)",
               (session["user_id"], title.strip()))
    return redirect("/")


@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
@login_required
def edit_todo(todo_id):
    title = request.form.get("title", "")
    error = validate_title(title)
    if error:
        return render_todos(edit_errors={todo_id: error}, edit_values={todo_id: title})
    db.execute("UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
               (title.strip(), todo_id, session["user_id"]))
    return redirect("/")


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
@login_required
def toggle_todo(todo_id):
    is_done = 1 if request.form.get("is_done") == "1" else 0
    db.execute("UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
               (is_done, todo_id, session["user_id"]))
    return redirect("/")


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
@login_required
def delete_todo(todo_id):
    db.execute("DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
               (todo_id, session["user_id"]))
    return redirect("/")


if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5000)), debug=False)
