import sqlite3

def exec_cmd(command):
    database = sqlite3.connect("database.db")
    cur = database.cursor()
    cur.execute(command)
    database.commit()
    database.close()

def db_build():
    exec_cmd("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password TEXT);")
    exec_cmd("""CREATE TABLE IF NOT EXISTS countries(name TEXT UNIQUE,
                                                     alpha-2 TEXT UNIQUE,
                                                     alpha-3 TEXT UNIQUE,
                                                     found INTEGER);""")
    exec_cmd("""CREATE TABLE IF NOT EXISTS countries_stat(name TEXT UNIQUE,
                                                          calling_code TEXT UNIQUE,
                                                          capital TEXT,
                                                          population INTEGER,
                                                          lang TEXT,
                                                          flag TEXT,
                                                          currency TEXT,
                                                          region TEXT);""")
    exec_cmd("""CREATE TABLE IF NOT EXISTS currency_exchange(currency_1 TEXT,
                                                             value_1 REAL,
                                                             currency_2 TEXT,
                                                             value_2 REAL);""")
    exec_cmd("""CREATE TABLE IF NOT EXISTS name(name TEXT,
                                                code TEXT,
                                                count INTEGER,
                                                age INTEGER);""")
