from flask import *
from flask_heroku import Heroku
from scripts import db, render as r

# Configure the app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ylxnjybhzusyza:986c8ebe22636585e47fc3a8ece04a72addf08ff9ff6cf452a865e799de4aed1@ec2-54-225-205-79.compute-1.amazonaws.com:5432/dept28qq0qvuch'
app.secret_key = "A very secret key"

# bind to app
heroku = Heroku(app)
db.init_app(app)

# ROUTES

@app.route('/')
def main():
   return redirect('chat')

@app.route('/chat', methods = ['GET', 'POST'])
def chat():
   username = request.cookies.get('username')

   if username != None and username != "":
      return r.renderContent('chat.html', name=username)
   return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
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
   if request.method == 'POST':
      db.log_msg(request.form['text'], request.cookies.get('username'))
   return db.get_all_messages()

@app.route('/notion', methods = ['GET', 'POST'])
def notion():
   return r.renderContent('notion.html')

if __name__ == '__main__':
   app.run(debug=True)
   