import sqlite3


conn = sqlite3.connect('database.db')
cur = conn.cursor()


def setting_up_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY,
        key CHAR(255),
        application CHAR(255),
        email_or_username CHAR(255),
        password CHAR(255),  
        user CHAR(255),  
        FOREIGN KEY(user) REFERENCES pin(hwid)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pin (
        id INTEGER PRIMARY KEY,
        pin_number CHAR(4),
        hwid CHAR(255) DEFAULT NULL
    )""")


def execute_query(query, params):
    cur.execute(query, params)
    conn.commit()

    return cur.fetchall()
