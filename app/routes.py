from flask import render_template, flash, redirect
from flask.helpers import url_for
from app import app, db, bcrypt
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Checks if email already registered
        users_with_same_email = User.query.filter_by(email=form.email.data).first()
        if len(users_with_same_email) > 0:
            flash(f'User with the same email already exists', 'error')
            return redirect(url_for('register'))

        # Adds user to database
        user = User(firstname=form.firstname.data.strip(), lastname=form.lastname.data.strip(), email=form.email.data.strip(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/rankings', methods=['GET', 'POST'])
def rankings():

    return render_template("rankings.html")