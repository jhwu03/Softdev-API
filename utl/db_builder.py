import sqlite3
import urllib.request, json
from utl import db_manager

def exec_cmd(command):
    '''Opens the database, runs the given sqlite3 command, and closes the database'''
    database = sqlite3.connect("database.db")
    cur = database.cursor()
    cur.execute(command)
    database.commit()
    database.close()

def add_countries():
    '''adds all the countries and their alpha-2 and alpha-3 codes to the database
    if they don't already exist'''
    u = urllib.request.urlopen("""https://restcountries.eu/rest/v2/?fields=name;alpha2Code;alpha3Code;region""")
    response = u.read()
    data = json.loads(response)
    for row in data:
        # print(row)
        if not db_manager.has_country(row['name']):
            db_manager.add_country(row['name'], row['alpha2Code'], row['alpha3Code'], row['region'])

def db_build():
    '''create all database tables if they do not already exist,
    and add all the countries to the countries list if it is not already there'''
    exec_cmd("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password TEXT);")
    exec_cmd("""CREATE TABLE IF NOT EXISTS countries(name TEXT UNIQUE COLLATE NOCASE,
                                                     alpha_2 TEXT UNIQUE,
                                                     alpha_3 TEXT UNIQUE,
                                                     region TEXT,
                                                     found INTEGER);""")
    exec_cmd("""CREATE TABLE IF NOT EXISTS stat(name TEXT UNIQUE COLLATE NOCASE,
                                                calling_code TEXT UNIQUE,
                                                capital TEXT,
                                                population INTEGER,
                                                lang TEXT,
                                                flag TEXT,
                                                currency TEXT,
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
        add_countries()
    db_manager.close_db(database)
