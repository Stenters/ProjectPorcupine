from flask import *
from flask_heroku import Heroku
from flask_socketio import SocketIO
from scripts import db, render as r, routeHandlers as rh
from datetime import datetime

# Configure the app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ylxnjybhzusyza:986c8ebe22636585e47fc3a8ece04a72addf08ff9ff6cf452a865e799de4aed1@ec2-54-225-205-79.compute-1.amazonaws.com:5432/dept28qq0qvuch'
app.secret_key = "A very secret key"

# bind to app
sio = SocketIO(app)
heroku = Heroku(app)
db.init_app(app)

# ROUTES

@app.route('/')
def main():
   return redirect('chat')

@app.route('/chat', methods = ['GET', 'POST'])
def chat():
   return rh.handle(request, rh.chat)

@app.route('/login', methods = ['GET', 'POST'])
def login():
   return rh.handle(request, rh.login)

@app.route('/message', methods = ['GET', 'POST'])
def message():
   return rh.handle(request, rh.message)

@app.route('/kanban', methods = ['GET', 'POST'])
def kanban():
   return rh.handle(request, rh.kanban)

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
   app.run(debug=True)
