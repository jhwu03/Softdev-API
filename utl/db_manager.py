import sqlite3

DB_FILE = "database.db"

def close_db(database):
    database.commit()
    database.close()

def add_login(username, password):
    if username == "" or password == "":
        return "Credentials cannot be left blank"
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    message = ""
    cur.execute("SELECT * FROM users WHERE user_name = ?;", (username,))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users(user_name, user_password) VALUES(?, ?);",
                    (username, password,))
    else:
        message = "Username already exists!"
    close_db(database)
    return message

def verify_login(username, password):
    if username == "" or password == "":
        return "Credentials cannot be left blank"
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    message = ""
    cur.execute("SELECT * FROM users WHERE user_name = ? AND user_password = ?;" , (username, password,))
    if cur.fetchone() is None:
        message = "Login credentials not found! Please try again."
    close_db(database)
    return message

def convert_currency(curr_1, value, curr_2):
    return ""

def reset_quiz():
    return ""

def get_name_stats(name, country):
    return ""

def has_name(name, country):
    return ""

def add_name(name, country, count, age):
    return ""

def get_alpha_2(country):
    return ""

def get_alpha_3(country):
    return ""

def has_currency(country_1, country_2):
    return ""

def add_currency(currency_1, currency_2, rate):
    return ""

def has_country(country):
    return ""

def add_country(country, calling_code, cap, pop, lang, flag, curr, reg):
    return ""

def search_country(keyword):
    return ""
