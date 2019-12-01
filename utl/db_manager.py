import sqlite3
from urllib.request import urlopen
import json
from utl import db_builder

DB_FILE = "database.db"

CURRENCY_LIST = ["AED", "ARS", "AUD", "BGN", "BRL", "BSD", "CAD", "CHF", "CLP", "CNY",
                 "COP", "CZK", "DKK", "DOP", "EGP", "EUR", "FJD", "GBP", "GTQ", "HKD",
                 "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "KZT", "MXN",
                 "MYR", "NOK", "NZD", "PAB", "PEN", "PHP", "PKR", "PLN", "PYG", "RON",
                 "RUB", "SAR", "SEK", "SGD", "THB", "TRY", "TWD", "UAH", "USD", "UYU",
                 "VND", "ZAR"]

def close_db(database):
    '''commits and close database changes'''
    database.commit()
    database.close()

def add_login(username, password):
    '''return empty string if login credentials are added successfully,
    else, return an error message to be flashed'''
    if username == "" or password == "":
    # if either the username or password field is blank, return an error message to be flashed
        return "Credentials cannot be left blank"
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    # open database
    message = ""
    cur.execute("SELECT * FROM users WHERE username = ?;", (username,))
    if cur.fetchone() is None:
    # if there are no users in the database with the same username,
        cur.execute("INSERT INTO users(username, password) VALUES(?, ?);",
                    (username, password,))
        # add the username and password into the database
    else:
        message = "Username already exists!"
    # else set message to an error message
    close_db(database)
    # close the database and return the error message (empty string if there is no error)
    return message

def verify_login(username, password):
    '''return empty string if login credentials are valid,
    else, return an error message to be flashed'''
    if username == "" or password == "":
    # if either the username or password field is blank, return an error message to be flashed
        return "Credentials cannot be left blank"
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    # open database
    message = ""
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?;",
                (username, password,))
    if cur.fetchone() is None:
    # if the username and password combo is not in the database, set the message to an error message
        message = "Login credentials not found! Please try again."
    close_db(database)
    # close database and return the error message (empty string if there is no error)
    return message

def convert_currency(curr_1, value, curr_2):
    '''return the value converted from curr_2 to curr_1,
    return -1 if an error occured (either value is negative or currency does not exist)'''
    if value < 0:
    # if the given value is less than 0, return -1
        return -1
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    # open database
    if not has_currency(curr_1, curr_2):
    # if conversion rate is not in database
        url = urlopen("https://api.exchangerate-api.com/v4/latest/" + curr_1)
        # open the api
        response = url.read()
        data = json.loads(response)['rates']
        # read in all the available currencies and conversion rate
        for curr in data:
        # recursively add all the currencies and conversion rates to the database
            if curr != curr_1:
            # exclude the original currency from this
                add_currency(curr_1, curr, data[curr])
    cur.execute("SELECT value_2 FROM currency WHERE currency_1 = ? AND currency_2 = ?;",
                (curr_1, curr_2,))
    # choose the conversion rate from the currency table in database
    rate = cur.fetchone()
    if rate is None:
    # if there is no rate for the given currencies, return -1
        return -1
    close_db(database)
    # close database and return the product of the value and rate
    return value * rate[0]

def reset_quiz(username):
    '''resets the quiz for a user by deleting all the rows in quiz table with the given username'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("DELETE FROM quiz WHERE name = ?;", (username,))
    close_db(database)

def get_name_stats(name, alpha_2):
    '''returns the number of people and average age of people with the name in the given country,
    returns a list with values 0 and null if stats does not exist'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    # open database
    if not has_name(name, alpha_2):
    # if the name and country combo is not in the database
        url = urlopen("https://api.agify.io/?name=" + name + "&country_id=" + alpha_2)
        # open the api
        response = url.read()
        data = json.loads(response)
        # get data from the api
        add_name(data['name'], data['country_id'], data['count'], data['age'])
        # add the data into the database
    cur.execute("SELECT count, age FROM name WHERE name = ? AND code = ?;",
                (name, alpha_2,))
    # select the count and age from the database
    data = []
    row = cur.fetchone()
    if row is not None:
    # if the data is not None,
        data = [row[0], row[1]]
        # add the count and age to a list
    close_db(database)
    # close database and return the list
    return data

def has_name(name, alpha_2):
    '''return True if the given name and country combo is in database'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM name WHERE name = ? AND code = ?;",
                (name, alpha_2,))
    data = cur.fetchone()
    close_db(database)
    return data != None

def add_name(name, country, count, age):
    '''if the given name and country is not already in database, add its stats into database'''
    if not has_name(name, country):
        database = sqlite3.connect(DB_FILE)
        cur = database.cursor()
        cur.execute("INSERT INTO name(name, code, count, age) VALUES(?, ?, ?, ?);",
                    (name, country, count, age,))
        close_db(database)

def get_alpha(country, type):
    '''returns either the alpha_2 or alpha_3 code for the given country,
    based on the type given (either "2" or "3")'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT alpha_" + type + " FROM countries WHERE name = ?;", (country,))
    ans = ""
    data = cur.fetchone()
    if data is not None:
        ans = data[0]
    close_db(database)
    return ans

def add_currency(currency_1, currency_2, rate):
    '''add the given currencies and their conversion rate into the database'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("""INSERT INTO currency(currency_1, value_1, currency_2, value_2)
                   VALUES(?, ?, ?, ?);""",
                (currency_1, 1, currency_2, rate,))
    cur.execute("UPDATE stat SET conversion = 1 WHERE currency = ?;", (currency_1,))
    close_db(database)

def get_currency(country):
    '''returns the currency code of the given country'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT currency FROM stat WHERE name =?;", (country,))
    data = cur.fetchone()[0]
    close_db(database)
    return data

def has_currency(currency_1, currency_2):
    '''returns true if conversion rate from currency_1 to currency_2 is in database'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM currency WHERE currency_1 = ? AND currency_2 = ?;",
                (currency_1, currency_2))
    data = cur.fetchone()
    close_db(database)
    return data != None

def get_currency_list(currency):
    '''returns the list of currencies in which the given currency can be converted into'''
    ans = []
    if currency in CURRENCY_LIST:
        ans = [x for x in CURRENCY_LIST if x != currency]
    return ans

def has_stat(country):
    '''returns True if the stats for the given country is in the database'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM stat WHERE name = ?;",
                (country,))
    data = cur.fetchone()
    close_db(database)
    return data != None

def add_stat(country, calling_code, cap, pop, lang, flag, curr):
    '''if the stats for the given country is not in the database, add it to the database'''
    if not has_stat(country):
        database = sqlite3.connect(DB_FILE)
        cur = database.cursor()
        cur.execute("""INSERT INTO stat(name, calling_code, capital, population,
                                        lang, flag, currency)
                       VALUES(?, ?, ?, ?, ?, ?, ?);""",
                    (country, calling_code, cap, pop, lang, flag, curr))
        close_db(database)

def has_country(country):
    '''returns true if country is in countries table in database'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM countries WHERE name = ?;",
                (country,))
    data = cur.fetchone()
    close_db(database)
    return data != None

def add_country(country, alpha_2, alpha_3, region):
    '''add given country to countries table if it is is not already there'''
    if not has_country(country):
        database = sqlite3.connect(DB_FILE)
        cur = database.cursor()
        cur.execute("""INSERT INTO countries(name, alpha_2, alpha_3, region)
                       VALUES(?, ?, ?, ?);""",
                    (country, alpha_2, alpha_3, region))
        close_db(database)

def search_country(keyword):
    ''' return a dictionary of all the countries that contains the keyword,
    with the key as the country name and value as the alpha-3 code'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT name, alpha_3 FROM countries WHERE name LIKE '%' || ? || '%';",
                (keyword,))
    data = {}
    for row in cur.fetchall():
        data[row[0]] = row[1]
    close_db(database)
    return data

def found_country(country, username):
    '''returns the country name if the given country is valid and is not already found
    returns an empty string if the country name is not valid or is already found by user'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT name, region FROM countries WHERE name = ?;", (country,))
    stat = cur.fetchone()
    cur.execute("SELECT * FROM quiz WHERE country = ? AND name = ?;", (country, username,))
    data = ""
    if stat is not None and cur.fetchone() is None:
        cur.execute("INSERT INTO quiz(name, country, region) VALUES(?, ?, ?)",
                    (username, stat[0], stat[1],))
        data = country
    close_db(database)
    return data

def get_found_countries(username):
    '''returns a dictionary of all the countries found by user,
    with the keys being the countries and the values being
    the region the country is in'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT country, region FROM quiz WHERE name = ?;", (username,))
    found_countries = {}
    for row in cur.fetchall():
        found_countries[row[0]] = row[1]
        print(row[1])
    close_db(database)
    return found_countries

def alpha_to_country(alpha_3):
    '''return the country name for the given alpha-3 code'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT name FROM countries WHERE alpha_3 = ?;", (alpha_3,))
    data = cur.fetchone()[0]
    close_db(database)
    return data

def get_country_stat(alpha_3):
    '''returns the country stats as a dictionary for the given alpha-3 code,
    return empty dictionary if stats are not found'''
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    # open database
    country = alpha_to_country(alpha_3)
    # set country to the name of the country with the alpha-3 code
    if not has_stat(country):
    # if the stats are not already in database
        url = urlopen("https://restcountries.eu/rest/v2/alpha/" + alpha_3 +
                      "?fields=name;callingCodes;capital;population;languages;currencies;flag")
        # open api
        response = url.read()
        data = json.loads(response)
        # load the json response
        currency = data['currencies'][0]['code']
        # set currency to the currency code
        add_stat(data['name'], data['callingCodes'][0], data['capital'], data['population'],
                 data['languages'][0]['name'], data['flag'], currency)
        # add all the stats pulled from api to the database
    cur.execute("""SELECT stat.name, alpha_2, alpha_3, calling_code, capital,
                population, lang, flag, currency, region FROM countries, stat
                WHERE stat.name = ? AND countries.name = ?;""",
                (country, country,))
    # get the stats for the given country
    data = {}
    row = cur.fetchone()
    if row is not None:
    # if stats exist, put them all into a dictionary with the key being the description of the value
        data = {"name": row[0], "alpha_2": row[1], "alpha_3": row[2],
                "calling_code": row[3], "capital": row[4],
                "population": row[5], "language": row[6], "flag": row[7],
                "currency": row[8], "region":row[9]}
    close_db(database)
    # close database and return dictionary
    return data
