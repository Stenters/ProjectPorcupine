from flask import *
from flask_heroku import Heroku
from flask_socketio import SocketIO
from scripts import db as DB, render as r, routeHandlers as rh
from datetime import datetime
import sys

# Configure the app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "A very secret key"

# bind to app
# sio = SocketIO(app, cors_allowed_origin='*')
sio = SocketIO(app)
heroku = Heroku(app)
Debug = '-d' in sys.argv
db = DB.Database(app, debug=Debug)

# ROUTES


@app.route('/')
def main():
   """
   Called if no route is entered
   """
   return redirect('chat')


@app.route('/chat', methods = ['GET', 'POST'])
def chat():
   """
   Main page, for chatting
   """
   username = request.cookies.get('username')

   if username != None and username != "":
      return r.renderContent('chat.html', name=username)
   return redirect('/login')


@app.route('/login', methods = ['GET', 'POST'])
def login():
   """
   Route for handling logging in
   """
   error = None
   
   if request.method == 'POST':
      if not db.login(request.form['username'], request.form['password']):
         error = 'Invalid username or password. Please try again!'
      else:
         resp = make_response(redirect(url_for('main')))
         resp.set_cookie('username', request.form['username'])
         resp.set_cookie('password', request.form['password'])
         return resp
   return r.renderContent('login.html', error = error)


@app.route('/message', methods = ['GET', 'POST'])
def message():
   """
   Route for posting messages or getting the pre-rendered html
   """
   if request.method == 'POST':
      db.log_msg(request.form['text'], request.cookies.get('username'))
   return db.get_all_messages()


@app.route('/kanban', methods = ['GET', 'POST'])
def kanban():
   """
   Method for showing kanban board
   """
   if request.method == 'GET':
      (todo, doing, done) = db.get_all_kanban()
      return r.renderContent('kanban.html', 
         todo=Markup(todo), doing=Markup(doing), done=Markup(done))
   else:
      db.log_kanban(request.form['status'], request.form['value'])
      return r.renderContent('kanban.html')

# Socket Events

def callback():
   print("emission recived")

@sio.on('status')
def printStatusMsg(msg):
   print(f"(Client) {msg}")
   sio.emit('response', db.get_all_messages(), callback=callback)

@sio.on('message')
def reciveMessage(message):
   print(f"logging message\n\tuser: {message['username']}\ttext: {message['text']}\n")
   db.log_msg(message['text'], message['username'])
   sio.emit('response', f"<p><strong>{message['username']}: </strong>{message['text']} <sub>{str(datetime.now())}</sub></p><br>\n", callback=callback)


if __name__ == '__main__':
   app.run(debug=Debug)
   print("db is " + str(db))
