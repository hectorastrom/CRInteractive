from flask import url_for, flash, redirect
from flask.helpers import url_for
from flask_login import current_user
from functools import wraps

# Coach Required Decorator 
def coach_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.coach_key == "000000":
            flash(f'Insufficient permissions', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def convert_2k(total, form):
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