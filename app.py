"""Flask app for Notes"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import db, connect_db, User, Note
from form import RegisterForm, LoginForm, NoteForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "THIS DOESNT MATTER"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.debug = True


toolbar = DebugToolbarExtension(app)

connect_db(app)


# ============================================================
# Base Routes
# ============================================================
@app.get("/")
def get_homepage():
    """Redirect to register page"""

    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Handles displaying and processing the register form."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.username
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Handles displaying and processing the login form."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.username
            return redirect(f"/users/{ user.username }")
        else:
            form.username.errors = [
                "Account not found. Check username and password."
            ]

    return render_template("login.html", form=form)


@app.post("/logout")
def logout_user():
    """Logout user by popping "user_id" from session, redirect to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("user_id", None)
        return redirect("/")
    else:
        raise Unauthorized("Invalid CSRF token.")


@app.get("/secret")
def get_secret():
    """Renders the secret page"""

    if "user_id" not in session:
        raise Unauthorized("Not authorized to access the secret.")

    return render_template("secret.html")


# ============================================================
# User Routes
# ============================================================


@app.get("/users/<username>")
def get_user_details(username):
    """Display information about a user. Users can only view their own details
    except for password.
    """

    authenticate(username)

    user = User.query.get(username)
    form = CSRFProtectForm()
    return render_template("user_details.html", user=user, form=form)


@app.post("/users/<username>/delete")
def delete_user(username):
    """Delete user and notes from db"""

    authenticate(username)

    form = CSRFProtectForm()
    if form.validate_on_submit():
        user = User.query.get(username)
        Note.query.filter_by(owner=username).delete()
        db.session.delete(user)

        db.session.commit()
        session.pop("user_id", None)
        return redirect("/")
    else:
        raise Unauthorized()


# ============================================================
# Note Routes
# ============================================================


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):
    """Display and processes note form for creating new notes."""

    authenticate(username)

    form = NoteForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=username)
        db.session.add(note)
        db.session.commit()
        return redirect(f"/users/{username}")

    else:
        return render_template("add_note.html", form=form)


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """Update a note and redirect to user details page"""

    note = Note.query.get_or_404(note_id)
    authenticate(note.owner)

    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()
        return redirect(f"/users/{note.owner}")

    else:
        return render_template("update_note.html", form=form)


@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Delete note and redirect to user details page"""

    note = Note.query.get_or_404(note_id)
    authenticate(note.owner)

    form = CSRFProtectForm()
    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{note.owner}")
    else:
        raise Unauthorized("Invalid CSRF token.")


def authenticate(username):
    if session.get("user_id") != username:
        raise Unauthorized()
