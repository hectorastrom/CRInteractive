from datetime import date
from sqlalchemy.orm import backref
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    team = db.Column(db.String(20), nullable=False, default='none')
    side = db.Column(db.String(10), nullable=False, default='none')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    coach_key = db.Column(db.String(6), nullable=False, default="000000")
    # Height is in inches
    height = db.Column(db.Integer())
    weight = db.Column(db.Integer())
    grade = db.Column(db.Integer())
    twoks = db.relationship('Twok', backref='rower', lazy=True)

    def __repr__(self):
        return f"User(Firstname: '{self.firstname}', Lastname: '{self.lastname}', Email: '{self.email}', Team: '{self.team}', Side: '{self.side}', Imagefile: '{self.image_file}')"

class Twok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seconds = db.Column(db.Float, nullable=False)
    date_completed = db.Column(db.Date, nullable=False, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"2k(seconds: '{self.seconds}', date_completed: '{self.date_completed}', user_id: '{self.user_id}')"


        