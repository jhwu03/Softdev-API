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
    if 'name' in request.args:
        #made a request to get info on name
        name_stats = db_manager.get_name_stats(request.args['name'], request.args['country'])
    return render_template("homepage.html", username=user, name_stats=name_stats)

@app.route("/search")
def search():
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for('login'))
        # redirect to login page
    results = []
    if 'keyword' in request.args:
        #gets the keyword from the search bar
        keyword = request.args['keyword']
        #defines keyword
        results = db_manager.search_country(keyword)
        #goes through the database and find countries that fit the keyword
        print(results)
    return render_template("results.html", results = results)
    #renders results.html and gives the list of results

@app.route("/quiz")
def quiz():
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for("login"))
        # redirect to login page
    response = ""
    if 'country' in request.args:
    #sees if they have submitted an answer
        country = request.args['country']
        #defines country with their answer
        if (db_manager.has_country(country)):
        #if database has the country then check it off in the database
            response = db_manager.found_country(country)
            #goes through database to see if the country is there. If it is then response is a string of the country name
    if 'reset' in request.args:
    #if the user wants to reset their quiz
        db_manager.reset_quiz()
        #resets quiz by setting all the found values of the countries back to zero
    return render_template("quiz.html", results = db_manager.get_found_countries(), response = response)
    #renders quiz.html giving the list of the found countries as results, as well as a response as to whether their answer was correct or incorrect

@app.route("/countries/<country>")
def countries(country):
    if "username" not in session:
    # if user is not logged in,
        return redirect(url_for("login"))
        # redirect to login page
    stats = db_manager.get_country_stat(country)
    #goes through the database to get the country stats
    currency_stats = ""
    #defines currency stats
    curr_1 = db_manager.get_currency(country)
    #goes through database to get the currency code of the country of the page the user is on
    valid_curr_rates = db_manager.get_currency_list(curr_1)
    #goes through database to get the valid currency list by which the API gives rates to
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
                currency_stats = "{} {} = {} {}".format(value, curr_1, db_manager.convert_currency(curr_1, value, curr_2), curr_2)
                #goes through the database to find the rate, and the database converts the two rates, the answer is defined to currency_stats
            else:
                currencry_stats = "Not convertable, did not enter a number."
    return render_template("country.html", stats = stats, currency_stats = currency_stats, valid_curr_rates = valid_curr_rates)
    #renders country.html with the dict of country stats, a string of currency stats, and a list of the valid currency exchanges

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
