from flask import *
from scripts import db
# from scripts import *

app = Flask(__name__)
app.secret_key = "A very secret key"
username = None

# ROUTES

@app.route('/')
def main():
   username = request.cookies.get('username')

   if username != None:
      return render_template('index.html', name = username)
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
   return render_template('login.html', error = error)


@app.route('/message', methods = ['GET', 'POST'])
def message():
   if request.method == 'POST':
      db.log_msg(request.form['text'], request.cookies.get('username'))
   return db.get_all_messages()


if __name__ == '__main__':
   app.run(debug=True) 