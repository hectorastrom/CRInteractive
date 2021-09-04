from flask import render_template, flash, redirect
from flask.helpers import url_for
from flask_login.utils import login_required
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Twok
from flask_login import login_user, current_user, logout_user

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logged in for {form.email.data}!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Incorrect credentials. Please check email and password.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    print(current_user)
    flash('Logged out user.', 'success')
    return redirect(url_for('index'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Adds user to database
        user = User(firstname=form.firstname.data.strip(), lastname=form.lastname.data.strip(), email=form.email.data.strip(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/rankings', methods=['GET', 'POST'])
@login_required
def rankings():
    userList = list()

    users = User.query.all()
    for user in users:
        userTwok = dict()
        userTwok["name"] = user.firstname + " " + user.lastname
        userTwok["twok"] = Twok.query.filter_by(user_id=user.id).first()
        
    
    sorted(userList, key=lambda x:x["twok".seconds])



    return render_template("rankings.html", users=userList)