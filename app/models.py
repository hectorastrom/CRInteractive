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
    password = db.Column(db.String(60), default="not set")
    uuid = db.Column(db.String(8))
    is_coach = db.Column(db.Boolean, default=False)
    is_head = db.Column(db.Boolean, default=False)
    is_coxswain = db.Column(db.Boolean, default=False)
    pinged = db.Column(db.Boolean, default=False)
    default_on = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)
    # Height is in inches
    height = db.Column(db.Integer())
    weight = db.Column(db.Integer())
    grade = db.Column(db.Integer())
    twoks = db.relationship('Twok', backref='rower', lazy=True)
    fiveks = db.relationship('Fivek', backref='rower', lazy=True)
    metric = db.relationship('Metric', backref='rower', lazy=True)

    def __repr__(self):
        if not self.deleted:
            status = "Active"
        else:
            status = "Deleted"
        return f"{status} User(Firstname: '{self.firstname}', Lastname: '{self.lastname}', Email: '{self.email}', Team: '{self.team}', Side: '{self.side}', Imagefile: '{self.image_file}', is_coach: '{self.is_coach}', is_coxswain: '{self.is_coxswain}', uuid: '{self.uuid}')"

class Twok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seconds = db.Column(db.Float, nullable=False)
    date_completed = db.Column(db.Date, nullable=False, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"2k(seconds: '{self.seconds}', date_completed: '{self.date_completed}', user_id: '{self.user_id}')"

class Fivek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seconds = db.Column(db.Float, nullable=False)
    date_completed = db.Column(db.Date, nullable=False, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"5k(seconds: '{self.seconds}', date_completed: '{self.date_completed}', user_id: '{self.user_id}')"

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), default="")
    name = db.Column(db.String(50), default="")
    desc = db.Column(db.Text)
    coach_rating = db.Column(db.Integer, default=50)
    coach_importance = db.Column(db.Integer, default=5)
    user_rating = db.Column(db.Integer, default=50)
    user_importance = db.Column(db.Integer, default=5)
    view_allowed = db.Column(db.Boolean, default=False)
    has_set = db.Column(db.Boolean, default=False)
    has_update = db.Column(db.Boolean, default=False)
    note = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Metric(Metric Name: 'f{self.name}', Coach Rating: '{self.coach_rating}', User Rating: '{self.user_rating}', User Importance: '{self.user_importance}', View Allowed: '{self.view_allowed}', Has Set: '{self.has_set}', user_id: '{self.user_id}', Note: '{self.note}')"

        