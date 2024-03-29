import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
import urllib.request, json
# import flask functions
from utl import db_manager, db_builder
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
    return render_template("login.html")
    # render login template


@app.route("/create-acc")
def create_account():
    if "username" in session:
    # if user is logged in,
        return redirect(url_for("home"))
        # redirect to homepage
    if len(request.args) == 3:
    # if users clicked the submit button on create account page
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
    return render_template("create-acc.html")
    # render create-account.html template

@app.route("/home")
def home():
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for("login"))
        # redirect to login page
    user = session["username"]
    #user is set to the person logged in
    name_stats = []
    name = ""
    country = ""
    response = " "
    if 'name' in request.args:
        #made a request to get info on name
        name = request.args['name']
        country = request.args['country']
        if name == "":
            response = "Please enter a name:"
        else:
            response = ""
            name_stats = db_manager.get_name_stats(name, db_manager.get_alpha(country, "2"))
    country_list = db_manager.get_name_country_list()
    new_country_list = []
    for i in country_list:
        new_country_list.append(db_manager.name_alpha_to_country(i))
    return render_template("homepage.html", username=user, name_stats=name_stats, country_list=new_country_list, response=response, name=name, country=country)

@app.route("/search")
def search():
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for('login'))
        # redirect to login page
    results = []
    if 'keyword' in request.args:
        keyword = request.args['keyword']
        results = db_manager.search_country(keyword)
        return render_template("results.html", results = results, title = "Results for \"{}\"".format(keyword))
    return render_template("results.html", results = results, title = "Results")


@app.route("/quiz")
def quiz():
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for("login"))
        # redirect to login page
    response = ""
    if 'reset' in request.args:
        db_manager.reset_quiz(session['username'])
    if 'country' in request.args:
        country = request.args['country']
        response = db_manager.found_country(country, session['username'])
    results = db_manager.get_found_countries(session['username'])
    return render_template("quiz.html", results = results, response = response, long = len(results))

@app.route("/countries/<country_code>")
def countries(country_code):
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for("login"))
        # redirect to login page
    stats = db_manager.get_country_stat(country_code)
    country = db_manager.alpha_to_country(country_code)
    currency_stats = ""
    curr_1 = db_manager.get_currency(country)
    valid_curr_rates = db_manager.get_currency_list(curr_1)
    curr_2 = ""
    if ('curr_2' in request.args):
        #made a request to change currencies
        if ('value' in request.args):
            #only converts if a value is given
            value = request.args['value']
            #defines value as the value that the user gives
            try:
                value = float(value)
                #needs to ensure that it can be converted into a double. gets converted to double if no error is given
            except:
                value = ""
                #if it does not return an empty string
            curr_2 = request.args['curr_2']
            #defines the second currency code
            if (value != ""):
                converted_val = db_manager.convert_currency(curr_1, value, curr_2)
                if value >= 0.01 or value == 0:
                    currency_stats = "{:.2f} {} = {:.2f} {}".format(value, curr_1, converted_val, curr_2)
                else:
                    currency_stats = "Not convertible, please enter a valid number."
                #goes through the database to find the rate, and the database converts the two rates, the answer is defined to currency_stats
            else:
                currency_stats = "Not convertable, did not enter a number."
    return render_template("country.html", stats = stats, currency_stats = currency_stats, valid_curr_rates = valid_curr_rates, curr_2=curr_2)

@app.route("/logout")
def logout():
    if "username" in session:
    # if user is logged in
        session.pop("username")
        # pop "username" from session (logging the user out)
    return redirect(url_for("login"))
    # redirect user back to login page

if __name__ == "__main__":
    db_builder.db_build()
    app.debug = True
    app.run()
