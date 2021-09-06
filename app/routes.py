from flask import render_template, url_for, flash, redirect, request
from flask.helpers import url_for
from app import app, db, bcrypt, teams
from app.forms import RegistrationForm, LoginForm, TwokForm, CoachRegistrationForm
from app.models import User, Twok, Technique
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date
from time import strftime, gmtime
from random import randint
from functools import wraps

# def create_users(amount):
#     for i in range(amount):
#         name = "test"+str(i)
#         email = name + "@test.com"
#         password = name
#         team = teams[0]
#         new_user = User(firstname=name, lastname=name, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'), team=team, side="Port")
#         db.session.add(new_user)
#         db.session.commit()
#         new_2k = Twok(seconds=randint(360, 480), date_completed=date.today(), user_id=new_user.id)
#         db.session.add(new_2k)
#         db.session.commit()
# # REAALLLLY DANGEROUS THIS CREATES 10 NEW USERS EVERYTIME THE PROGRAM IS RUN WHICH IS DANGEROUS BAD BAD NEWS
# db.drop_all()
# db.create_all()
# create_users(30)

# Coach Required Decorator 
def coach_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.coach_key == "000000":
            flash(f'Insufficient permissions', 'danger')
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    # if current_user.coach_key != "000000":
    #     pass
    # else:
    #     return render_template('index.html')
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in for {form.email.data}!', 'success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            flash(f'Incorrect credentials. Please check email and password.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Adds user to database
        user = User(firstname=form.firstname.data.strip().capitalize(), lastname=form.lastname.data.strip().capitalize(), email=form.email.data.strip(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    possible_feet = [1,2,3,4,5,6,7]
    possible_inches = [0,1,2,3,4,5,6,7,8,9,10,11]
    user_inches = -1
    user_feet = -1
    if current_user.height:
        user_feet = int(current_user.height / 12)
        user_inches = int(current_user.height % 12)
    grades = [9, 10, 11, 12]
    if request.method == "POST":
        if current_user.coach_key == "000000":
            side = request.form.get("side")
            team = request.form.get("team")
            grade = request.form.get("grade")
            weight = request.form.get("weight")
            feet = request.form.get("feet")
            inches = request.form.get("inch")
            if not side:
                flash('Side not selected.', 'error')
                return redirect(url_for('settings'))
            if not team:
                flash('Team not selected.', 'error')
                return redirect(url_for('settings'))
            if not grade:
                flash('Grade not selected.', 'error')
                return redirect(url_for('settings'))
            if weight:
                current_user.weight = weight
            if feet and inches:
                if int(feet) and int(inches) in possible_inches:
                    current_user.height = int(feet) * 12 + int(inches)

            current_user.side = side
            current_user.team = team
            current_user.grade = int(grade)
        
        else:
            team = request.form.get("team")
            if not team:
                flash('Team not selected.', 'error')
                return redirect(url_for('settings'))
            current_user.team = request.form.get("team")

        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template("settings.html", teams=teams, possible_feet=possible_feet, possible_inches=possible_inches, grades=grades, user_feet = user_feet, user_inches = user_inches)

@app.route('/profile/<id>')
@login_required
def profile(id):
    user = User.query.get(int(id))
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('profile.html', image_file = image_file, user = user)

@app.route('/rankings', methods=['GET'])
@login_required
def rankings():
    userList = list()
    users = User.query.filter_by(team = current_user.team).all()

    labels = []
    values = []

    border_colors = []
    background_colors = []

    if users:
        for user in users:
            userTwok = dict()
            userTwok["name"] = user.firstname + " " + user.lastname
            userTwok["twok"] = Twok.query.filter_by(user_id=user.id).order_by("seconds").first()
            userTwok["id"] = user.id
            if userTwok['twok']:
                userTwok['date'] = userTwok['twok'].date_completed
                userTwok['twok'] = userTwok['twok'].seconds
                
                userList.append(userTwok)
        userList.sort(key=lambda x:x["twok"])
        for user in userList:
            if user['twok']:
                # This adds the name and 2k (in seconds!) of the user to labels and vlaues to be used in the chart
                labels.append(user["name"])
                # If the user is in the userList database, set that color value to be purple
                if user["id"] == current_user.id:
                    border_colors.append('rgb(144, 15, 209)')
                    background_colors.append('rgba(144, 15, 209, 0.25)')
                else:
                    border_colors.append('rgb(177, 23, 49)')
                    background_colors.append('rgba(177, 23, 49, 0.25)')

                values.append(user["twok"])

                time = user['twok']
                user['twok'] = strftime("%M:%S", gmtime(time))
    else:
        userTwok = dict()
        userTwok["name"] = "No user data found"
        userTwok["twok"] = " "
        userList.append(userTwok)



    return render_template("rankings.html", users = userList, labels = labels, values = values, border_colors = border_colors, background_colors = background_colors)

@app.route('/2k', methods=['GET', 'POST'])
@login_required
def upload_twok():
    form = TwokForm()
    if form.validate_on_submit():
        total_seconds = int(form.minutes.data)*60 + form.seconds.data
        twok = Twok(seconds=total_seconds, date_completed=form.date.data, user_id = current_user.id)
        db.session.add(twok)
        db.session.commit()
        flash(f'Logged 2K for {form.date.data}.', 'success')
        return redirect(url_for('index'))
    return render_template('2k.html', form=form)

@app.route('/register/coach', methods=['GET', 'POST'])
def coach_register():
    form = CoachRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Adds user to database
        user = User(firstname=form.firstname.data.strip(), lastname=form.lastname.data.strip(), email=form.email.data.strip(), password=hashed_password, coach_key=form.coach_key.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('registercoach.html', form=form)

@app.route('/roster')
@login_required
def roster():
    if current_user.coach_key != "000000":
        athletes = User.query.filter(User.team==current_user.team, User.coach_key == "000000").order_by(User.lastname).all()
        return render_template('roster.html', athletes=athletes)
    else:
        flash("You do not have permissions to access that page.", "error")
        return redirect(url_for('index'))