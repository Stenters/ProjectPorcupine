from flask import *
from flask_heroku import Heroku
from scripts import db, render as r, routeHandlers as rh


# Method for centralizing route handlers
def handle(request, route):
    if request.cookies.get('username') in (None, ''):
        return login(request)
    else:
        return route(request)


### Route Handlers ###


# Route handler for logging in a user
def login(request):
    error = None
   
    if request.method == 'POST':

      if not db.login(request.form['username'], request.form['password']):
         error = 'Invalid username or password. Please try again!'
      
      else:
      
        resp = make_response(redirect(url_for('chat')))
        resp.set_cookie('username', request.form['username'])
        resp.set_cookie('password', request.form['password'])
      
        return resp
    
    return r.renderContent('login.html', error = error)
    # return render_template('login.html', error = error)


# Route handler for the chat page
def chat(request):
    return r.renderContent('chat.html', name=request.cookies.get('username'))


# Route handler for posting or getting a message
def message(request):
    if request.method == 'POST':
        db.log_msg(request.form['text'], request.cookies.get('username'))
    return db.get_all_messages()


# Route handler for posting or getting kanban board
def kanban(request):
    if request.method == 'GET':
        (todo, doing, done) = db.get_all_kanban()

        return r.renderContent('kanban.html', todo=Markup(todo), doing=Markup(doing), done=Markup(done))

    else:
        db.log_kanban(request.form['status'], request.form['value'])
        return r.renderContent('kanban.html')
   