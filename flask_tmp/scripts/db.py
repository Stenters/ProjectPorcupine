import sqlite3
import threading
from passlib.hash import sha256_crypt as hash
from datetime import datetime

lock = threading.Lock()

def do_sql(sql, args = None):
    with sqlite3.connect('app.db') as con:
        try:
            lock.acquire()
            db = con.cursor()
            if args != None:
                db.execute(sql, args)
            else:
                db.execute(sql)
            con.commit()
            return db.fetchall()
        finally:
            lock.release()


def log_msg(msg, author):
    do_sql("""INSERT INTO messages (msg, author, time)
                    VALUES (?,?,?);""", (msg, author, str(datetime.now())))

def get_all_messages():
    res = ""

    for msg in do_sql("SELECT * FROM messages;"):
        res += f"<p><strong>{msg[2]}: </strong>{msg[1]} <sub>{msg[3]}</sub></p><br>\n"
    
    return res

def create_table():
    do_sql("""CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        msg VARCHAR(1024),
        author VARCHAR(255),
        time VARCHAR(255));""")
    do_sql("""CREATE TABLE IF NOT EXISTS login(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255),
        password VARCHAR(1024));""")

def login(username, password):
    res = do_sql("SELECT password from login where username=?;", (username,))
    
    if len(res) != 0:
        return hash.verify(password, res[0][0])
    else:
        return False


def create_user(username, password):
    password = hash.encrypt(password)
    do_sql("INSERT INTO login (username, password) VALUES (?,?)", (username, password))