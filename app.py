import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
# import flask functions
from data import db_manager, db_builder
# import database functions
app = Flask(__name__)
app.secret_key = os.urandom(32)
# set up sessions with random secret key

@app.route("/")
def root():
    if "username" in session:
    #if user is logged in,
        return redirect(url_for("home"))
        # redirect to homepage
    return redirect(url_for("login"))
    # else, redirect to login page


@app.route("/login")
def login():
    if "username" in session:
    # if user is logged in,
        return redirect(url_for("home"))
        # redirect to homepage
    if len(request.args) == 2:
    # if users clicked the log in button,
        if request.args["username"] == "" or request.args["password"] == "":
        # if either username or password is blank
            flash("Please do not leave any fields blank")
            # flash error
        else:
            response = db_manager.verify_login(request.args["username"],
                                               request.args["password"])
            # verify entered username and password with database
            if response == "":
            # if username and password combo is in database
                session["username"] = request.args["username"]
                # add username to session (log user in)
                return redirect(url_for("home"))
                # redirect to homepage
            else:
            # else is username/password is incorrect
                flash(response)
                # flash error
    return render_template("login/login.html")
    # render login template


@app.route("/create-account")
def create_account():
    if "username" in session:
    # if user is logged in,
        return redirect(url_for("home"))
        # redirect to homepage
    if len(request.args) == 3:
    # if users clicked the submit button on create account page
        if request.args["username"] == "" or request.args["passwordNew"] == "" or request.args["passwordRepeat"] == "":
        # if any one of the three fields are blank,
            flash("Please do not leave any fields blank")
            # flash an error
        else:
            if request.args["passwordNew"] != request.args["passwordRepeat"]:
            # if the two passwords do not match,
                flash("Passwords don't match, try again")
                # flash an error
            else:
            # else if the passwords match
                response = db_manager.add_login(request.args["username"],
                                                request.args["passwordNew"])
                # check with database to see if the username is valid/unique
                if response == "":
                # if username is valid,
                    session["username"] = request.args["username"]
                    # add username to session (log user in)
                    return redirect(url_for("login"))
                    # redirect to login page
                else:
                # else if the username is already taken
                    flash(response)
                    # flash error
    return render_template("login/create-account.html")
    # render create-account.html template

@app.route("/home")
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for("login"))
        # redirect to login page
    user = session["username"]
    #user is set to the person logged in
    return render_template("home.html", username=user)

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/countries")
def countries():
    return render_template("countries.html")


@app.route("/logout")
def logout():
    if "username" in session:
    # if user is logged in
        session.pop("username")
        # pop "username" from session (logging the user out)
    return redirect(url_for("login"))
    # redirect user back to login page

if __name__ == "__main__":
    app.debug = True
    app.run()
