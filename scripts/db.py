from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt as hash
from datetime import datetime

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

class User(db.Model):
    __tablename__ = "login"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(1024))

    def __init__(self, username, password):
        self.username = username
        self.password = hash.encrypt(password)

    def __repr__(self):
        return f"<id={self.id}, username={self.username}, password={self.password}>"

    def compare (self, password):
        return hash.verify(password, self.password)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(1024))
    author = db.Column(db.String(255))
    time = db.Column(db.String(255))

    def __init__(self, msg, author):
        self.msg = msg
        self.author = author
        self.time = str(datetime.now())

    def __repr__(self):
        return f"<id='{self.id}', msg='{self.msg}', author='{self.author}', time='{self.time}'>"


def log_msg(msg, author):
    db.session.add(Message(msg, author))
    db.session.commit()

def get_all_messages():
    res = ""

    for msg in db.session.query(Message).all():
        res += f"<p><strong>{msg.author}: </strong>{msg.msg} <sub>{msg.time}</sub></p><br>\n"

    return res

def login(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    return user.compare(password)

def create_user(username, password):
    db.session.add(User(username, password))
    db.session.commit()

# lock = threading.Lock()

# def do_sql(sql, args = None):
#     with sqlite3.connect('app.db') as con:
#         try:
#             lock.acquire()
#             db = con.cursor()
#             if args != None:
#                 db.execute(sql, args)
#             else:
#                 db.execute(sql)
#             con.commit()
#             return db.fetchall()
#         finally:
#             lock.release()


# def log_msg(msg, author):
#     do_sql("""INSERT INTO messages (msg, author, time)
#                     VALUES (?,?,?);""", (msg, author, str(datetime.now())))

# def get_all_messages():
#     res = ""

#     for msg in do_sql("SELECT * FROM messages;"):
#         res += f"<p><strong>{msg[2]}: </strong>{msg[1]} <sub>{msg[3]}</sub></p><br>\n"
    
#     return res

# def create_table():
#     do_sql("""CREATE TABLE IF NOT EXISTS messages(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         msg VARCHAR(1024),
#         author VARCHAR(255),
#         time VARCHAR(255));""")
#     do_sql("""CREATE TABLE IF NOT EXISTS login(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username VARCHAR(255),
#         password VARCHAR(1024));""")

# def login(username, password):
#     res = do_sql("SELECT password from login where username=?;", (username,))
    
#     if len(res) != 0:
#         return hash.verify(password, res[0][0])
#     else:
#         return False


# def create_user(username, password):
#     password = hash.encrypt(password)
#     do_sql("INSERT INTO login (username, password) VALUES (?,?)", (username, password))