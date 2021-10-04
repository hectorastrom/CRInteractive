from random import randint
from flask import url_for, flash, redirect
from flask.helpers import url_for
from flask_login import current_user
from functools import wraps
from app import db
from app.models import User

# Coach Required Decorator 
def coach_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_coach:
            flash(f'Insufficient permissions', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def convert_from_seconds(total, form):
    if form == "split":
        split_seconds = total/4
        minutes = int(split_seconds/60)
        seconds = round(split_seconds % 60, 1)
    else:
        minutes = int(total/60)
        seconds = round(total % 60, 1)

    if seconds < 10:
            seconds = "0" + str(seconds)
    return str(minutes) + ":" + str(seconds)

def create_account(firstname, lastname, email, role, team):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return (existing_user, "exists")
    else:
        if team.lower() == "mv":
            team = "Men's Varsity"
        elif team.lower() == "l" or team.lower() == "fl":
            team = "Fall Launchpad"
        elif team.lower() != "men's varsity" and team.lower() != "fall launchpad":
            # Unrecognized team names default to launchpad
            team = "Fall Launchpad"
        unique_id = randint(10000000, 99999999)
        while User.query.filter_by(uuid=str(unique_id)).first():
            unique_id = randint(10000000, 99999999)
        unique_id = str(unique_id)
        user = User(firstname=firstname, lastname=lastname, email=email, team=team, uuid=unique_id)
        if role.lower() == "coxswain":
            user.is_coxswain = True
        elif role.lower() == "coach":
            user.is_coach = True
        db.session.add(user)
        db.session.commit()
        return (user, "added")

class MetricObj():
    def __init__(self, tag, name, desc=""):
        self.tag = tag
        self.name = name
        self.desc = desc
    def __repr__(self) -> str:
        return f'*Tag: {self.tag}, Name: {self.name}, Description: {self.desc}*'
