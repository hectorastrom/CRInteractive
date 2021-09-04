from flask import render_template, flash, redirect
from flask.helpers import url_for
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Twok

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Logged in for {form.email.data}.', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.firstname.data}.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)