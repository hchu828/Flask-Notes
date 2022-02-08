"""Flask app for Notes"""

from flask import Flask, render_template, request, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from form import RegisterForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "THIS DOESNT MATTER"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.debug = True


toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.get("/")
def get_homepage():
    """Redirect to register"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def create_user():

    form = RegisterForm()

    if form.validate_on_submit():
        pass

    else:
        return render_template("register.html", form=form)
