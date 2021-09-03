from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy.orm import backref

import os



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['secret_key']
bcrypt = Bcrypt()
# To hash do bycrypt.generate_password_hash(password).decode('utf-8')
# To check password do bycrypt.check_password_hash(hashed_password, password)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    team = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    twoks = db.relationship('Twok', backref='rower', lazy=True)

    def __repr__():
        return f"User(Firstname: '{self.firstname}', Lastname: '{self.lastname}', Email: '{self.email}', Team: '{self.team}', Imagefile: '{self.imagefile}')"

class Twok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seconds = db.Column(db.Float, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__():
        return f"2k(seconds: '{self.seconds}', date_uploaded: '{self.date_uploaded}', user_id: '{self.user_id}')"
        

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)