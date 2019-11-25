import sqlite3
import urllib.request, json
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

def get_name_stats(name, alpha_2):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    if not has_name(name, alpha_2):
        url = urllib.request.urlopen("https://api.agify.io/?name=" + name + "&country_id=" + alpha_2)
        response = url.read()
        data = json.loads(response)
        add_name(data['name'], data['country_id'], data['count'], data['age'])
    cur.execute("SELECT count, age FROM name WHERE name = ? AND code = ?;",
                (name, alpha_2,))
    data = []
    row = cur.fetchone()
    if row is not None:
        data = [row[0], row[1]]
    close_db(database)
    return data

def has_name(name, alpha_2):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM name WHERE name = ? AND code = ?;",
                (name, alpha_2,))
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

def add_currency(currency_1, currency_2, rate):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("""INSERT INTO currency(currency_1, value_1, currency_2, value_2)
                   VALUES(?, ?, ?, ?);""",
                (currency_1, 1, currency_2, rate,))
    cur.execute("UPDATE stat SET conversion = 1 WHERE currency = ?;", (currency_1,))
    close_db(database)

def get_currency(country):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT currency FROM stat WHERE name =?;", (country,))
    data = cur.fetchone()[0]
    close_db(database)
    return data

def get_currency_list(currency):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT conversion FROM stat WHERE currency = ?;", (currency,))
    has_curr = cur.fetchone()[0]
    if has_curr == 2:
        return []
    if has_curr == 0:
        url = urllib.request.urlopen("https://api.exchangerate-api.com/v4/latest/" + currency)
        response = url.read()
        data = json.loads(response)['rates']
        for curr in data:
            if curr != currency:
                add_currency(currency, curr, data[curr])
    cur.execute("SELECT currency_2 FROM currency WHERE currency_1 = ?;", (currency,))
    data = []
    for curr in cur.fetchall():
        data.append(curr[0])
    close_db(database)
    return data

def has_stat(country):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("SELECT * FROM stat WHERE name = ?;",
                (country,))
    data = cur.fetchone()
    close_db(database)
    return data != None

def add_stat(country, calling_code, cap, pop, lang, flag, curr, reg, has_curr):
    if not has_stat(country):
        database = sqlite3.connect(DB_FILE)
        cur = database.cursor()
        cur.execute("""INSERT INTO stat(name, calling_code, capital, population,
                                        lang, flag, currency, region, conversion)
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                    (country, calling_code, cap, pop, lang, flag, curr, reg, has_curr))
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
    cur.execute("SELECT name FROM countries WHERE name LIKE '%' || ? || '%';",
                (keyword,))
    data = []
    for row in cur.fetchall():
        data.append(row[0])
    close_db(database)
    return data

def found_country(country):
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("UPDATE countries SET found = 1 WHERE name = ?;", (country,))
    close_db(database)

def get_found_countries():
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    cur.execute("""SELECT stat.name, region FROM stat, countries
                WHERE countries.name = stat.name AND found = 1;""")
    africa = []
    americas = []
    asia = []
    europe = []
    oceania = []
    for row in cur.fetchall():
        if row[1] == 'Africa':
            africa.append(row[0])
        if row[1] == 'Americas':
            americas.append(row[0])
        if row[1] == 'Asia':
            asia.append(row[0])
        if row[1] == 'Europe':
            europe.append(row[0])
        if row[1] == 'Oceania':
            oceania.append(row[0])
    close_db(database)
    return {"Africa": africa, "Americas": americas,
            "Asia": asia, "Europe": europe, "Oceania": oceania}

def get_country_stat(country):
    country_url = country.replace(" ", "%20")
    database = sqlite3.connect(DB_FILE)
    cur = database.cursor()
    if not has_stat(country):
        url = urllib.request.urlopen("https://restcountries.eu/rest/v2/name/" + country_url +
                                     "?fields=name;callingCodes;capital;population;languages;currencies;flag;region")
        response = url.read()
        data = json.loads(response)[0]
        has_curr = 0
        currency = data['currencies'][0]['code']
        try:
            urllib.request.urlopen("https://api.exchangerate-api.com/v4/latest/" + currency)
        except Exception as e:
            has_curr = 2
        add_stat(data['name'], data['callingCodes'][0], data['capital'], data['population'],
                 data['languages'][0]['name'], data['flag'], currency,
                 data['region'], has_curr)
    cur.execute("""SELECT stat.name, alpha_2, alpha_3, calling_code, capital,
                population, lang, flag, currency, region FROM countries, stat
                WHERE stat.name = ? AND countries.name = ?;""",
                (country, country,))
    data = {}
    row = cur.fetchone()
    if row is not None:
        data = {"name": row[0], "alpha_2": row[1], "alpha_3": row[2],
                "calling_code": row[3], "capital": row[4],
                "population": row[5], "language": row[6], "flag": row[7],
                "currency": row[8], "region":row[9]}
    close_db(database)
    return data
