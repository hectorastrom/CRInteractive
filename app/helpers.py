from flask import url_for, flash, redirect
from flask.helpers import url_for
from flask_login import current_user
from time import strftime, gmtime
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

def convert_2k(seconds, form):
    if form == "split":
        time = seconds/4
        time = strftime("%M:%S", gmtime(time))
    else:
        time = seconds
        time = strftime("%M:%S", gmtime(time))
    return time