from datetime import date
import datetime
from sqlalchemy.orm import backref
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
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
    date_created = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    # Height is in inches
    height = db.Column(db.Integer())
    weight = db.Column(db.Integer())
    grade = db.Column(db.Integer())
    twoks = db.relationship('Twok', backref='rower', lazy=True)
    fiveks = db.relationship('Fivek', backref='rower', lazy=True)
    metric = db.relationship('Metric', backref='rower', lazy=True)
    status = db.relationship('Status', backref='rower', lazy=True)

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

# Metric is a depreciated table
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
    has_update = db.Column(db.Boolean, default=True)
    for_coxswain = db.Column(db.Boolean, default=False)
    note = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Metric(Metric Name: 'f{self.name}', Coach Rating: '{self.coach_rating}', User Rating: '{self.user_rating}', User Importance: '{self.user_importance}', View Allowed: '{self.view_allowed}', Has Set: '{self.has_set}', user_id: '{self.user_id}', Note: '{self.note}')"

# Entries are forever stored for all entries. Compared to Metrics, these also
# do not store redundant information such as name, desc, or tag
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coach_rating = db.Column(db.Integer, nullable=False)
    coach_importance = db.Column(db.Integer, nullable=False)
    user_rating = db.Column(db.Integer)
    view_allowed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    coach_id = db.Column(db.Integer)
    note = db.relationship('EntryNote', backref='entry', lazy=True)
    empmetric_id = db.Column(db.Integer, db.ForeignKey('empmetrics.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"""
        Entry({self.id})
        CoachRating: {self.coach_rating}
        CoachImp: {self.coach_importance}
        UserRating: {self.user_rating}
        DateCreated: {self.date_created}
        EmpMetricId: {self.empmetric_id}
        UserId: {self.user_id}
        """

# Notes stored separately since most Entries won't have notes
class EntryNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)

    def __repr__(self) -> str:
        return f"""EntryNote({self.id}), Content: '{self.content}', EntryId: {self.entry_id}"""

class EmpMetrics(db.Model):
    __tablename__ = 'empmetrics'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(5), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.Text)
    team = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    for_cox = db.Column(db.Boolean, default=False)
    entries = db.relationship('Entry', backref='empmetrics', lazy=True)

    def __repr__(self):
        return f"""
        EmpMetric({self.id})
        Tag: {self.tag}
        Name: {self.name}
        Description: '{self.desc}'
        Team: {self.team}
        Active: {self.active}
        ForCox: {self.for_cox}
        """


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text)
    mood = db.Column(db.Integer)
    sleep = db.Column(db.Text)
    sickness = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

        