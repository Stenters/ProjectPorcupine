from flask_sqlalchemy import SQLAlchemy, Model
from passlib.hash import sha256_crypt as hash
from datetime import datetime
from sqlalchemy import Column, String, Integer

db = SQLAlchemy()

class Database:

    def __init__(self,app, **kwargs):
        '''
        Initialize the database (with the Flask object)
        '''
        if ('debug' in kwargs and kwargs['debug'] == True):
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgres://ylxnjybhzusyza:986c8ebe22636585e47fc3a8ece04a72addf08ff9ff6cf452a865e799de4aed1@ec2-54-225-205-79.compute-1.amazonaws.com:5432/dept28qq0qvuch'

        db.init_app(app)
        self.app = app


    def log_msg(self, msg, author):
        '''
        Log a message to the database
        '''
        with self.app.app_context():
            db.session.add(Message(msg, author))
            db.session.commit()


    def get_all_messages(self):
        '''
        Get all messages from the database
        '''
        res = ""

        with self.app.app_context():
            for msg in db.session.query(Message).all():
                res += f"<p><strong>{msg.author}: </strong>{msg.msg} <sub>{msg.time}</sub></p><br>\n"

        return res


    def login(self, username, password):
        '''
        Check if a username and passwod is valid
        '''
        with self.app.app_context():
            user = db.session.query(User).filter_by(username=username).first()
        return user != None and user.compare(password)


    def create_user(self, username, password):
        '''
        Create a new user account
        '''
        with self.app.app_context():
            db.session.add(User(username, password))
            db.session.commit()


    def log_kanban(self, status, value):
        '''
        Create a new Kanban item or update the status of one 
        (if it is doing or done, remove it from the old column and add it to the new one)
        '''
        with self.app.app_context():
            if status == "doing":
                prev = Kanban.query.filter_by(value=value, status="todo").first()
                db.session.delete(prev)
            if status == "done":
                prev = Kanban.query.filter_by(value=value, status="doing").first()
                db.session.delete(prev)
            db.session.add(Kanban(status, value))
            db.session.commit()


    def get_all_kanban(self):
        '''
        Get all the Kanban items from the database
        '''
        todo = ''
        doing = ''
        done = ''
        
        with self.app.app_context():
            for resp in db.session.query(Kanban).all():
                if resp.status == "todo":
                    todo += '<p class="kanban-item kanban-todo">' + resp.value + '</p>'
                elif resp.status == "doing":
                    doing += '<p class="kanban-item kanban-doing">' + resp.value + '</p>'
                else:
                    done += '<p class="kanban-item kanban-done">' + resp.value + '</p>'

        return (todo, doing, done)


    def getDB(self):
        return db

    ### Modles ###


class User(db.Model):
    '''
    A DB object to represent a user
    '''
    __tablename__ = "login"
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(1024))

    def __init__(self, username, password):
        self.username = username
        self.password = hash.encrypt(password)

    def __repr__(self):
        return f"<id={self.id}, username={self.username}, password={self.password}>"

    def compare (self, password):
        return hash.verify(password, self.password)


class Message(db.Model):
    '''
    A DB object to represent a message
    '''
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    msg = Column(String(1024))
    author = Column(String(255))
    time = Column(String(255))

    def __init__(self, msg, author):
        self.msg = msg
        self.author = author
        self.time = str(datetime.now())

    def __repr__(self):
        return f"<id='{self.id}', msg='{self.msg}', author='{self.author}', time='{self.time}'>"


class Kanban(db.Model):
        '''
        A DB object to represent a kanban card
        '''
        __tablename__ = "kanban"
        id = Column(Integer, primary_key=True)
        status = Column(String(5))
        value = Column(String(1024))

        def __init__(self, status, value):
            self.status = status
            self.value = value
            
        def __repr__(self):
            return f"<id='{self.id}', status='{self.status}', value='{self.value}'>"




### Old code for reference ###




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