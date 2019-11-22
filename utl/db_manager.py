import sqlite3
from utl import db_builder

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
    if value < 0:
        return -1
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT value_2 FROM currency WHERE currency_1 = ? AND currency_2 = ?;",
                (curr_1, curr_2,))
    rate = cur.fetchone()
    if rate is None:
        return -1
    close_db(database)
    return value * rate[0]

def reset_quiz():
    db_builder.exec_cmd("UPDATE countries SET found = 0;")

def get_name_stats(name, country):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT count, age FROM name WHERE name = ? AND code = ?;",
                (name, country,))
    data = []
    row = cur.fetchone()
    if row is not None:
        data = [row[0], row[1]]
    close_db(database)
    return data

def has_name(name, country):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM name WHERE name = ? AND code = ?;",
                (name, country,))
    data = cur.fetchone()
    close_db(database)
    return data != None

def add_name(name, country, count, age):
    if not has_name(name, country):
        database = sqlite3.connect(DB_FILE)
        cur = database.cursor()
        cur.execute("INSERT INTO name(name, code, count, age) VALUES(?, ?, ?, ?);",
                    (name, country, count, age,))
        close_db(database)

def get_alpha(country, type):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT alpha_" + type + " FROM countries WHERE name = ?;", (country,))
    ans = ""
    data = cur.fetchone()
    if data is not None:
        ans = cur.fetchone()[0]
    close_db(database)
    return ans

def has_currency(currency_1, currency_2):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM currency WHERE currency_1 = ? AND currency_2 = ?;",
                (currency_1, currency_2,))
    data = cur.fetchone()
    close_db(database)
    return data != None

def add_currency(currency_1, currency_2, rate):
    if not has_currency(currency_1, currency_2):
        database = sqlite3.connect(DB_FILE)
        cur = database.cursor()
        cur.execute("""INSERT INTO currency(currency_1, value_1, currency_2, value_2)
                       VALUES(?, ?, ?, ?);""",
                    (currency_1, 1, currency_2, rate,))
        close_db(database)

def has_stat(country):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM stat WHERE name = ?;",
                (country,))
    data = cur.fetchone()
    close_db(database)
    return data != None

def add_stat(country, calling_code, cap, pop, lang, flag, curr, reg):
    if not has_stat(country):
        database = sqlite3.connect(DB_FILE)
        cur = database.cursor()
        cur.execute("""INSERT INTO stat(name, calling_code, capital, population,
                                        lang, flag, currency, region)
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?);""",
                    (country, calling_code, cap, pop, lang, flag, curr, reg))
        close_db(database)

def has_country(country):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM countries WHERE name = ?;",
                (country,))
    data = cur.fetchone()
    close_db(database)
    return data != None

def add_country(country, alpha_2, alpha_3):
    if not has_country(country):
        database = sqlite3.connect(DB_FILE)
        cur = database.cursor()
        cur.execute("""INSERT INTO countries(name, alpha_2, alpha_3, found)
                       VALUES(?, ?, ?, ?);""",
                    (country, alpha_2, alpha_3, 0))
        close_db(database)

def search_country(keyword):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT name FROM stat WHERE name LIKE '%' || ? || '%';",
                (keyword,))
    data = []
    for row in cur.fetchall():
        data.append(row[0])
    close_db(database)
    return data

def found_country(country):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("UPDATE countries SET found = 0 WHERE name = ?;", (country,))

def get_found_countries():
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    africa = []
    cur.execute("SELECT name FROM stat WHERE region = 'Africa'")
    for row in cur.fetchall():
        africa.append(row[0])
    americas = []
    cur.execute("SELECT name FROM stat WHERE region = 'Americas'")
    for row in cur.fetchall():
        americas.append(row[0])
    asia = []
    cur.execute("SELECT name FROM stat WHERE region = 'Asia'")
    for row in cur.fetchall():
        asia.append(row[0])
    europe = []
    cur.execute("SELECT name FROM stat WHERE region = 'Europe'")
    for row in cur.fetchall():
        europe.append(row[0])
    oceania = []
    cur.execute("SELECT name FROM stat WHERE region = 'Oceania'")
    for row in cur.fetchall():
        oceania.append(row[0])
    return {"Africa": africa, "Americas": americas,
            "Asia": asia, "Europe": europe, "Oceania": oceania}
