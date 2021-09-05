from flask import render_template, url_for, flash, redirect, request
from flask.helpers import url_for
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, TwokForm
from app.models import User, Twok
from flask_login import login_user, current_user, logout_user, login_required
from time import strftime, gmtime

@app.route("/")
def index():
    if current_user.coach_key != "000000":
        pass
    else:
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
        user = User(firstname=form.firstname.data.strip(), lastname=form.lastname.data.strip(), email=form.email.data.strip(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    teams = ["Varsity Mens", "Mens U17"]
    if request.method == "POST":
        side = request.form.get("side")
        team = request.form.get("team")
        weight = request.form.get('weight')
        height = request.form.get('height')
        if not side:
            flash('Side not selected.', 'error')
            return redirect(url_for('settings'))
        if not team:
            flash('Team not selected.', 'error')
            return redirect(url_for('settings'))
        if not weight and not current_user.weight:
            flash('Weight not specified', 'error')
            return redirect(url_for('settings'))
        if not height and not current_user.height:
            flash('Height not specified', 'error')
            return redirect(url_for('settings'))

        current_user.side = request.form.get("side")
        current_user.team = request.form.get("team")
        current_user.weight = request.form.get('weight')
        current_user.height = request.form.get('height')
        
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template("settings.html", teams = teams)

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
    users = User.query.all()

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

