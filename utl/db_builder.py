import sqlite3
import urllib.request, json
from utl import db_manager

def exec_cmd(command):
    database = sqlite3.connect("database.db")
    cur = database.cursor()
    cur.execute(command)
    database.commit()
    database.close()

def add_regions(region):
    u = urllib.request.urlopen("https://restcountries.eu/rest/v2/region/" +
                               region + "?fields=name;alpha2Code;alpha3Code")
    response = u.read()
    data = json.loads(response)
    for row in data:
        if not db_manager.has_country(row['name']):
            db_manager.add_country(row['name'], row['alpha2Code'], row['alpha3Code'])

def db_build():
    exec_cmd("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password TEXT);")
    exec_cmd("""CREATE TABLE IF NOT EXISTS countries(name TEXT UNIQUE,
                                                     alpha_2 TEXT UNIQUE,
                                                     alpha_3 TEXT UNIQUE,
                                                     found INTEGER);""")
    exec_cmd("""CREATE TABLE IF NOT EXISTS stat(name TEXT UNIQUE,
                                                calling_code TEXT UNIQUE,
                                                capital TEXT,
                                                population INTEGER,
                                                lang TEXT,
                                                flag TEXT,
                                                currency TEXT,
                                                region TEXT,
                                                conversion INTEGER);""")
    exec_cmd("""CREATE TABLE IF NOT EXISTS currency(currency_1 TEXT,
                                                    value_1 REAL,
                                                    currency_2 TEXT,
                                                    value_2 REAL);""")
    exec_cmd("""CREATE TABLE IF NOT EXISTS name(name TEXT,
                                                code TEXT,
                                                count INTEGER,
                                                age INTEGER);""")
    database = sqlite3.connect("database.db")
    cur = database.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM countries);")
    if cur.fetchone()[0] == 0:
        for region in ["africa", "americas", "asia", "europe", "oceania"]:
            add_regions(region)
    db_manager.close_db(database)
