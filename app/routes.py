from flask import render_template, url_for, flash, redirect, request
from flask.helpers import url_for
from app import app, db, bcrypt, teams
from app.forms import RegistrationForm, LoginForm, TwokForm, CoachRegistrationForm
from app.models import User, Twok, Fivek, Metric
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date
from random import randint
from app.helpers import convert_from_seconds, coach_required, MetricObj
from app.static.metrics import rower_metric_list, cox_metric_list


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"], strict_slashes=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.password != "not set":
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
        elif user and user.password == "not set":
            flash(f"Account for {form.email.data} is not yet initalized. Head to the registration link in your email to finish creating your account.", "error")
        else: 
            flash(f"Acccount registed with {form.email.data} does not exist.", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=["GET", "POST"], strict_slashes=False)
def search_code():
    if request.method == "POST":
        potential_user = User.query.filter_by(uuid=request.form.get("search_code")).first()
        if potential_user:
            return redirect(url_for("register", uuid=request.form.get("search_code")))
        else: 
            flash("Invalid Code. Please try again.", "error")
            return redirect("")
    else:
        random_num = randint(10000000, 99999999)
        return render_template("search_uuid.html", random_num=random_num)

@app.route('/register/<uuid>', methods=["GET", "POST"])
def register(uuid):
    user = User.query.filter(User.uuid==uuid).first()
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        login_user(user, remember=True)
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('index'))
    else:
        if not user:
            flash("Registration page for that code does not exist.", "error")
            return redirect(url_for("search_code"))
        elif user and user.password != "not set":
            flash("Account has already been created.", "error")
            return redirect(url_for("login"))
        else:
            return render_template("register.html", form=form, user=user)



@app.route('/settings', methods=["GET", "POST"], strict_slashes=False)
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
        if not current_user.is_coach:
            if not current_user.is_coxswain:
                side = request.form.get("side")
                if not side:
                    flash('Side not selected.', 'error')
                    return redirect(url_for('settings'))
                current_user.side = side
            grade = request.form.get("grade")
            weight = request.form.get("weight")
            feet = request.form.get("feet")
            inches = request.form.get("inch")
            if not grade:
                flash('Grade not selected.', 'error')
                return redirect(url_for('settings'))
            if weight:
                current_user.weight = weight
            if feet and inches:
                if int(feet) and int(inches) in possible_inches:
                    current_user.height = int(feet) * 12 + int(inches)
            current_user.grade = int(grade)
        else:
            team = request.form.get("team")
            default_on = bool(request.form.get("enable_default"))
            if not team:
                flash('Team not selected.', 'error')
                return redirect(url_for('settings'))
            current_user.team = team
            current_user.default_on = default_on

        flash('Settings Updated.', 'success')

        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template("settings.html", teams=teams, possible_feet=possible_feet, possible_inches=possible_inches, grades=grades, user_feet = user_feet, user_inches = user_inches)
    

@app.route('/profile/<firstname>:<id>', methods=["GET", "POST"], strict_slashes=False)
@login_required
def profile(firstname, id):
    user = User.query.filter(User.firstname==firstname.capitalize(), User.id==id).first()
    if not user:
        flash("Profile not found", 'error')
        return redirect(url_for('index'))
    if request.method == "POST":
        # For non-coaches the only form is requesting a review 
        if not current_user.is_coach:
            if not current_user.pinged:
                current_user.pinged = True
                db.session.commit()
                flash("Review has been requested.", "success")
            return redirect('#')
        else:
            if request.form.get("form_identifier") == "silence":
                user.pinged = False
                db.session.commit()
                flash("Request has been silenced.", "success")
                return redirect('#')
            else:
                # Get the metric with the name of the form identifier that was submitted
                updated_metric = Metric.query.filter(Metric.user_id == id, Metric.tag == request.form.get("form_identifier")).first()
                # If nothing was found, which could happen if the user inspects element, then it won't continue
                if not updated_metric:
                    flash("Problem submitting form. Please try again.", "error")
                    return redirect(request.url)

                if not updated_metric.has_set:
                    updated_metric.has_set = True
                updated_metric.coach_rating = request.form.get(f"{updated_metric.tag}_coach_rating")
                updated_metric.coach_importance = request.form.get(f"{updated_metric.tag}_coach_importance")
                updated_metric.note = request.form.get(f"{updated_metric.tag}_coach_notes")
                updated_metric.view_allowed = bool(request.form.get(f"{updated_metric.tag}_view_allowed"))
                db.session.commit()
                flash(f"Updated {updated_metric.name} for {user.firstname}.", "success")
                return redirect('#')
    else:
        if user.is_coxswain:
            focused_list = cox_metric_list
        else:
            focused_list = rower_metric_list
        # Goes through and adds all important metrics for a user if they don't exist when a coach is viewing
        if current_user.is_coach:
            for defMetric in focused_list:
                metric = Metric.query.filter(Metric.user_id==id, Metric.tag==defMetric.tag, Metric.name==defMetric.name).first()
                if not metric:
                    if current_user.default_on:
                        metric = Metric(user_id=id, tag=defMetric.tag, name=defMetric.name, view_allowed = True, desc=defMetric.desc)
                    else:
                        metric = Metric(user_id=id, tag=defMetric.tag, name=defMetric.name, desc=defMetric.desc)
                    db.session.add(metric)
                    db.session.commit()
        # All metrics is to be sent to profiles to be displayed
        # The purpose of a for loop instead of querying Metrics with user_id.all() is that metrics that have had their name changed or removed will not longer appear as metrics to view.
        all_metrics = []
        for metric in focused_list:
            new_metric = Metric.query.filter(Metric.user_id==id, Metric.tag==metric.tag).first()
            if new_metric is not None:
                all_metrics.append(new_metric)
        all_user_metrics = []
        for metric in focused_list:
            new_metric = Metric.query.filter(Metric.user_id==id, Metric.tag==metric.tag, Metric.name==metric.name, Metric.has_set==True, Metric.view_allowed==True).first()
            if new_metric is not None:
                all_user_metrics.append(new_metric)
        image_file = url_for('static', filename='profile_pics/' + user.image_file)
        twok = Twok.query.filter_by(user_id=id).order_by("seconds").first()
        if twok:
            twok = convert_from_seconds(twok.seconds, "time")
        else:
            twok = "No Data"
        fivek = Fivek.query.filter_by(user_id=id).order_by("seconds").first()
        if fivek:
            fivek = convert_from_seconds(fivek.seconds, "time")
        else:
            fivek = "No Data"
        if current_user.is_coach:
            return render_template('coach_profile.html', image_file = image_file, user=user, all_metrics=all_metrics, twok=twok, fivek=fivek)
        else:
            return render_template('user_profile.html', image_file = image_file, user=user, all_metrics=all_user_metrics, twok=twok, fivek=fivek)


@app.route('/2k', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def upload_twok():
    form = TwokForm()
    if form.validate_on_submit():
        total_seconds = int(form.minutes.data)*60 + form.seconds.data
        twok = Twok(seconds=total_seconds, date_completed=form.date.data, user_id = current_user.id)
        db.session.add(twok)
        db.session.commit()
        flash(f'Logged 2k for {form.date.data}.', 'success')
        return redirect(url_for('index'))
    return render_template('2k.html', form=form)


@app.route('/5k', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def upload_fivek():
    form = TwokForm()
    if form.validate_on_submit():
        total_seconds = int(form.minutes.data)*60 + form.seconds.data
        fivek = Fivek(seconds=total_seconds, date_completed=form.date.data, user_id = current_user.id)
        db.session.add(fivek)
        db.session.commit()
        flash(f'Logged 5k for {form.date.data}.', 'success')
        return redirect(url_for('index'))
    return render_template('5k.html', form=form)


@app.route('/roster', strict_slashes=False)
@login_required
def roster():
    if current_user.is_coach:
        athletes = User.query.filter(User.team==current_user.team, User.is_coach == False).order_by(User.pinged.desc(), User.lastname).all()

        return render_template('roster.html', athletes=athletes)
    else:
        flash("You do not have permissions to access that page.", "error")
        return redirect(url_for('index'))

@app.route('/edit-roster', strict_slashes=False)
@login_required
def edit_roster():
    if current_user.is_coach:
        athletes = User.query.filter(User.team==current_user.team, User.is_coach == False).order_by(User.id).all()
        return render_template('edit_roster.html', athletes=athletes)
    else:
        flash("You do not have permissions to access that page.", "error")
        return redirect(url_for('index'))

@app.route('/aboutus', strict_slashes=False)
def about_us():
    hector_image = url_for('static', filename='profile_pics/' + 'default.jpg') # Replace with photo for hector 
    albert_image = url_for('static', filename='profile_pics/' + 'default.jpg') # Replace with photo for albert 
    return render_template("about_us.html", hector_image = hector_image, albert_image = albert_image)       


@app.route('/forgotpass', methods=["GET","POST"], strict_slashes=False)
def forgotpass():
    if request.method == "POST":
        email = request.form.get("email")
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash(f"Password reset email sent to {email}.")
        else:
            flash("No account registered with that email. Please try again using a different email.", "error")
            return redirect("")
        return redirect(url_for("login"))
    else:
        return render_template("forgotpass.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", url = request.url), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", url = request.url), 500
    
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, server_error)

