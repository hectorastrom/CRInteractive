from flask import render_template, url_for, flash, redirect, request
from flask.helpers import url_for
from app import app, db, bcrypt, teams
from app.forms import RegistrationForm, LoginForm, TwokForm, CoachRegistrationForm
from app.models import User, Twok, Fivek, Metric
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date
from random import randint
from app.helpers import convert_from_seconds, coach_required, MetricObj

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

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user.password != "not set":
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
        else:
            flash(f"Account for {user.email} is not yet initalized. Head to the registration link in your email to finish creating your account.", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=["GET", "POST"])
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
            return redirect(url_for("index"))
        elif user and user.password != "not set":
            flash("Account has already been created.", "error")
            return redirect(url_for("login"))
        else:
            return render_template("register.html", form=form, user=user)



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
        if not current_user.is_coach:
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
    

# MetricObjs have format tag, name, description. Descriptions are default "" so they can be omitted.
rower_metric_list = [
    MetricObj("gt", "General Technique", "Coaches' subjective estimate of your technique."),
    MetricObj("bp", "Body Preparation", "Are arms fully extended, lats slightly engaged, spine supported, and shoulders forward of hips prior to quarter slide?"),
    MetricObj("rhythm", "Rhythm", "Distance Over Time = Speed. Distance = Connected Length. Power * Connected Length = Distance Over Time."),
    MetricObj("sync", "Synchronicity", "Doing the same thing as everyone else at the same time."),
    MetricObj("enspd", "Entry Speed", "The time it takes for your blade to go from piercing the water’s surface to being at the optimal depth (top edge just under surface). Theoretically, perfect entry occurs at full arc, a.k.a. the point of farthest reach."),
    MetricObj("drvmech", "Drive Mechanics", "Does the force you apply to the footboard move the boat and the rowers in it forwards or backwards?"),
    MetricObj("bldlock", "Blade Lock", "Does your blade stay at the same depth throughout the whole drive?"),
    MetricObj("release", "Release", "Do you complete the drive before feathering or applying downward pressure on the handle? Is the pressure off the blade before you remove it from the water?"),
    MetricObj("hands", "Hands", "Do you use your inside wrist for the feather completely, or do you let the oarlock take over? Is your inside hand and arm relaxed when you square the blade and take the catch?"),
    MetricObj("gp", "General Physiology", "Overall, less precise measure of physiology."),
    MetricObj("pe", "Power Endurance", "Box jumps, bat mans, KB swings, pull-ups, truck pushes, 2k erg etc."),
    MetricObj("ae", "Aerobic Endurance", "Stadium times, consistency in long rows, bi- or tri-athlons: anything longer than 20 minutes."),
    MetricObj("mob", "Mobility", "Full range of motion at the ankle, knee, hip, shoulder without compensatory movement anywhere else in your body, especially in your spine."),
    MetricObj("bm", "Breath Mechanics", "Do you maintain core stability when you’re breathing hard, or not? Are you able to remain un-shrugged all throughout long rows?")
]

cox_metric_list = [
    MetricObj("pe", "Practice Efficiency", "Duration of practice transitions, getting boats on and off racks/water, spinning / aligning boats done without wasting time."),
    MetricObj("pex", "Practice Execution", "Is your crew executing the prescribed drills properly on the first try? Do you rotate through pairs in sync with the coaches' and other boats' clocks? Is your crew at the prescribed rates the entire time?"),
    MetricObj("tex", "Technical Execution", "How do your blades look? Are they skying? Missing water? Staying locked at the right depth? Are your stations catching and finishing together? Is your crew checking the boat, or picking it up on the fly?"),
    MetricObj("st", "Steering", "Do you stay close to the other eight (when applicable)? Do you know how to maneuver around obstacles without disrupting the flow of practice? Do you stay on the right side of the river at all times?"),
    MetricObj("candc", "Clarity and Conciceness", "In how few words are you able to get your message across? How easy is it for your crew to understand your commands? Is there unnecessary, meaningless filler?"),
]
@app.route('/profile/<firstname>:<id>', methods=["GET", "POST"])
@login_required
def profile(firstname, id):
    user = User.query.filter(User.firstname==firstname.capitalize(), User.id==id).first()
    if not user:
        flash("Profile not found", 'error')
        return redirect(url_for('index'))
    if request.method == "POST":
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
                updated_metric.view_allowed = bool(request.form.get(f"{updated_metric.tag}_view_allowed"))
                db.session.commit()
                flash(f"Updated {updated_metric.tag} for {user.firstname}.", "success")
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


@app.route('/2k', methods=['GET', 'POST'])
@login_required
def upload_twok():
    form = TwokForm()
    if form.validate_on_submit():
        total_seconds = int(form.minutes.data)*60 + form.seconds.data
        twok = Twok(seconds=total_seconds, date_completed=form.date.data, user_id = current_user.id)
        db.session.add(twok)
        db.session.commit()
        flash(f'Logged 5k for {form.date.data}.', 'success')
        return redirect(url_for('index'))
    return render_template('2k.html', form=form)


@app.route('/5k', methods=['GET', 'POST'])
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


@app.route('/roster')
@login_required
def roster():
    if current_user.is_coach:
        athletes = User.query.filter(User.team==current_user.team, User.is_coach == False).order_by(User.pinged.desc(), User.lastname).all()

        return render_template('roster.html', athletes=athletes)
    else:
        flash("You do not have permissions to access that page.", "error")
        return redirect(url_for('index'))

@app.route('/aboutus')
def about_us():
    hector_image = url_for('static', filename='profile_pics/' + 'default.jpg') # Replace with photo for hector 
    albert_image = url_for('static', filename='profile_pics/' + 'default.jpg') # Replace with photo for albert 
    return render_template("about_us.html", hector_image = hector_image, albert_image = albert_image)        

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", url = request.url), 404
    
app.register_error_handler(404, page_not_found)

