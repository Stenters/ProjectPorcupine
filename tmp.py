from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku

app = Flask( __name__ )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///enterss'
heroku = Heroku(app)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lname = db.Column(db.String(50))

    def __init__ (self, name, lname=''):
        self.name = name
        self.lname = lname

    def __repr__(self):
        return f"<id={self.id}, name={self.name}, lname={self.lname}"

@app.route("/")
def enter_data():
    users = db.session.query(User).all()
    return render_template("dataentry.html", users=users)

@app.route("/submit", methods=["POST"])
def post_to_db():
    name = request.form['name']
    lname = request.form['lname']
    try:
        db.session.add(User(name, lname))
        db.session.commit()
    except Exception as e:
        print(e)
        sys.stdout.flush()
    return 'Success! To enter more data, <a href="{}">click here!</a>'.format(url_for("enter_data"))    


if __name__ == "__main__":
    app.debug = True
    app.run()


