import sqlite3
from db_builder import exec_cmd

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
    cur.execute("SELECT * FROM users WHERE username = ?;", (username,))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users(username, password) VALUES(?, ?);",
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
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?;",
                (username, password,))
    if cur.fetchone() is None:
        message = "Login credentials not found! Please try again."
    close_db(database)
    return message

def convert_currency(curr_1, value, curr_2):
    return ""

def reset_quiz():
    exec_cmd("UPDATE countries SET found = 0;")

def get_name_stats(name, country):
    return ""

def has_name(name, country):
    return ""

def add_name(name, country, count, age):
    return ""

def get_alpha(country, type):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT alpha_" + type + " FROM countries WHERE name = ?;", (country,))
    ans = cur.fetchone()[0]
    close_db(database)
    return ans

def has_currency(currency_1, currency_2):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM currency WHERE currency_1 = ? AND currency_2 = ?",
                (currency_1, currency_2,))
    return cur.fetchall() != None

def add_currency(currency_1, currency_2, rate):
    return ""

def has_country(country):
    return ""

def add_country(country, calling_code, cap, pop, lang, flag, curr, reg):
    return ""

def search_country(keyword):
    return ""
