from flask import render_template, url_for, flash, redirect, request
from flask.helpers import url_for
from app import app, db, bcrypt, teams, is_production
from app.forms import RegistrationForm, LoginForm, TwokForm, CoachRegistrationForm
from app.models import EmpMetrics, User, Twok, Fivek, Metric
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date, datetime
from random import randint
from app.helpers import convert_from_seconds, coach_required, MetricObj, create_account, create_email, email_links, chooseRole
from app.static.metrics import rower_metric_list, cox_metric_list


@app.route("/")
def index():
    if current_user.is_authenticated and not current_user.is_coach:
        return redirect(url_for('profile', firstname=current_user.firstname.lower(), id=current_user.id))
    elif current_user.is_authenticated and current_user.is_coach:
        return redirect(url_for('roster'))
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"], strict_slashes=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email==form.email.data.lower()).first()
        if user and user.deleted:
            flash(f'Account deactivated.', 'error')
            return redirect(url_for('login'))
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
        potential_user = User.query.filter(User.uuid==request.form.get("search_code")).first()
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
        user.date_created = datetime.utcnow()
        user.deleted = False
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
                elif side != "Port" and side != "Starboard" and side != "BothS" and side != "BothP":
                    flash('Invalid input.', 'error')
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
                try:
                    weight = int(weight)
                    current_user.weight = weight
                except:
                   flash('Invalid weight input.', 'error')
                   return redirect(url_for('settings')) 
            if feet and inches:
                try:
                    if int(feet) in possible_feet and int(inches) in possible_inches:
                        current_user.height = int(feet) * 12 + int(inches)
                    else: 
                        flash('Invalid height inputs.', 'error')
                        return redirect(url_for('settings'))
                except:
                   flash('Height inputs must be numeric.', 'error')
                   return redirect(url_for('settings'))
            current_user.grade = int(grade)
            total_name = current_user.firstname + " " + current_user.lastname
            input_name = request.form.get("namecap")
            if input_name.lower() != total_name.lower():
                flash("Name does not match original name. For name changes outside of capitalization contact your head coach.", "error")
                return redirect(url_for('settings'))
            space_index = input_name.index(" ")
            input_firstname = input_name[:space_index]
            input_lastname = input_name[space_index+1:]
            if input_firstname[0].islower() or input_lastname.islower():
                flash("Invalid capitalization of name.", "error")
                return redirect(url_for('settings'))
            current_user.firstname = input_firstname
            current_user.lastname = input_lastname
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
        team_names = teams.keys()
        return render_template("settings.html", teams=team_names, possible_feet=possible_feet, possible_inches=possible_inches, grades=grades, user_feet = user_feet, user_inches = user_inches)
    

@app.route('/profile/<firstname>:<id>', methods=["GET", "POST"], strict_slashes=False)
@login_required
def profile(firstname, id):
    user = User.query.filter(User.firstname.ilike(firstname), User.id==id, User.deleted == False).first()
    if not user:
        flash("Profile not found", 'error')
        return redirect(url_for('roster'))
    if request.method == "POST":
        # Different forms for coaches and non-coaches
        if not current_user.is_coach:
            if request.form.get("form_identifier") == "ping":
                current_user.pinged = True
                db.session.commit()
                flash("Review has been requested.", "success")
                return redirect('')
            else:
                requested_metric = Metric.query.filter(Metric.user_id == id, Metric.tag == request.form.get("form_identifier")).first()
                if not requested_metric:
                    flash("Problem submitting form. Please try again.", "error")
                    return redirect(request.url)
                requested_metric.user_rating = request.form.get(f"{requested_metric.tag}_user_rating")
                requested_metric.has_update = False
                db.session.commit()
                flash(f"You may now view coach's rating for {requested_metric.name}.", "success")
                return redirect('')
        # If the user is a coach: 
        else:
            if request.form.get("form_identifier") == "silence":
                user.pinged = False
                db.session.commit()
                flash("Request has been silenced.", "success")
                return redirect('')
            else:
                # Get the metric with the name of the form identifier that was submitted
                updated_metric = Metric.query.filter(Metric.user_id == id, Metric.tag == request.form.get("form_identifier")).first()
                # If nothing was found, which could happen if the user inspects element, then it won't continue
                if not updated_metric:
                    flash("Problem submitting form. Please try again.", "error")
                    return redirect(request.url)
                note = request.form.get(f"{updated_metric.tag}_coach_notes").strip()
                if "`" in note:
                    flash(f"Note for {updated_metric.name} may not contain the character `.", "error")
                    return redirect(request.url)
                updated_metric.coach_rating = request.form.get(f"{updated_metric.tag}_coach_rating")
                updated_metric.coach_importance = request.form.get(f"{updated_metric.tag}_coach_importance")
                updated_metric.note = note
                updated_metric.view_allowed = bool(request.form.get(f"{updated_metric.tag}_view_allowed"))
                updated_metric.has_set = True
                # When there's an update available, a user should have to indicate their rating
                updated_metric.has_update = True
                db.session.commit()
                flash(f"Updated {updated_metric.name} for {user.firstname}.", "success")
                return redirect('')
    else:
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

        if current_user.id != user.id and not current_user.is_coach:
            return render_template('user_profile.html', image_file = image_file, user=user, twok=twok, fivek=fivek)
        
        if user.is_coxswain:
            for_coxswain = True
            focused_list = cox_metric_list
        else:
            for_coxswain = False
            focused_list = rower_metric_list
        # Goes through and adds all important metrics for a user if they don't exist when a coach is viewing
        if current_user.is_coach:
            for defMetric in focused_list:
                metric = Metric.query.filter(Metric.user_id==id, Metric.tag==defMetric.tag, Metric.name==defMetric.name).first()
                if not metric:
                    if current_user.default_on:
                        metric = Metric(user_id=id, tag=defMetric.tag, name=defMetric.name, view_allowed = True, desc=defMetric.desc, for_coxswain=for_coxswain)
                    else:
                        metric = Metric(user_id=id, tag=defMetric.tag, name=defMetric.name, desc=defMetric.desc, for_coxswain=for_coxswain)
                    db.session.add(metric)
                    db.session.commit()
            # All metrics is to be sent to profiles to be displayed
            # The purpose of a for loop instead of querying Metrics with user_id.all() is that metrics that have had their name changed or removed will not longer appear as metrics to view.
            all_metrics = []
            for metric in focused_list:
                new_metric = Metric.query.filter(Metric.user_id==id, Metric.tag==metric.tag, Metric.name==metric.name).first()
                if new_metric is not None:
                    if new_metric.desc != metric.desc:
                        new_metric.desc = metric.desc
                        db.session.commit()
                    all_metrics.append(new_metric)

        all_user_metrics = []
        if user.id == current_user.id:
            for metric in focused_list:
                new_metric = Metric.query.filter(Metric.user_id==id, Metric.tag==metric.tag, Metric.name==metric.name, Metric.has_set==True, Metric.view_allowed==True).first()
                if new_metric is not None:
                    new_metric.desc = metric.desc
                    db.session.commit()
                    all_user_metrics.append(new_metric)
            # Sort user displayed metrics by their importance
            all_user_metrics.sort(key=lambda x:x.coach_importance, reverse=True)
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
    # Coaches renders roster
    if current_user.is_coach:
        users = User.query.filter(User.team==current_user.team, User.is_coach == False, User.deleted == False).order_by(User.pinged.desc(), User.lastname).all()
        # Athletes is a dictionary of all users on the coach's roster and their status of if all metrics are set.
        athletes = {}
        for user in users:
            for_coxswain = False
            if user.is_coxswain:
                for_coxswain = True
            incomplete_metric = Metric.query.filter(Metric.user_id == user.id, Metric.has_set == False, Metric.for_coxswain == for_coxswain).first()
            # Need an any metric since if they have not had metrics created yet then they will also have 0 incomplete metrics.
            any_metric = Metric.query.filter(Metric.user_id == user.id, Metric.for_coxswain == for_coxswain).first()
            if incomplete_metric or not any_metric:
                status = "incomplete"
            else:
                status = "set"
            athletes[user] = status
        # This turns athletes into a list of tuples sorted by incomplete or not
        athletes = sorted(athletes.items(), key=lambda x: x[1])
            
        return render_template('roster.html', athletes=athletes)
    # Rowers render team
    else:
        users = User.query.filter(User.team==current_user.team, User.is_coach == False, User.deleted == False).order_by(User.lastname).all()
        return render_template("team.html", users=users)

@app.route('/edit-roster', methods=["GET", "POST"], strict_slashes=False)
@login_required
def edit_roster():
    # List of team names
    team_names = teams.keys()
    # Valid Role inputs
    valid_roles = ["rower", "coxswain", "coach", "hcoach"]

    if request.method == "POST":
        form_identifier = request.form.get("form_identifier")
        if form_identifier:
            user = User.query.get(int(form_identifier[5:]))
            if form_identifier[:5] == "euser":
                user.firstname = request.form.get("firstname")
                user.lastname = request.form.get("lastname")
                role = request.form.get("role")
                if not role or role not in valid_roles:
                    flash("Invalid input for role.", "error")
                    return redirect("")
                chooseRole(user, role)

                team = request.form.get("team")
                if not team or team not in team_names:
                    flash("Invalid input for team.", "error")
                    return redirect("")
                user.team = team

                db.session.commit()
                flash(f"Updated Information for {user.firstname}.", "success")
                return redirect(request.url)
            elif form_identifier[:5] == "duser":
                user.deleted = True
                db.session.commit()
                flash(f"Deleted account for {user.firstname}.", "success")
                return redirect(request.url)
        else:
            firstname = request.form.get("firstname").strip()
            lastname = request.form.get("lastname").strip()
            email = request.form.get("email").lower().strip()
            role = request.form.get("role")
            team = request.form.get("team")
            if not firstname:
                flash("Must specify value for first name.", "error")
                return redirect("")
            if not lastname:
                flash("Must specify value for last name.", "error")
                return redirect("")
            if not email:
                flash("Must specify value for email.", "error")
                return redirect("")
            if not role:
                flash("Must specify value for role.", "error")
                return redirect("")
            if role not in valid_roles:
                flash("Invalid input for role.", "error")
                return redirect("")
            if not team:
                flash("Must specify value for team.", "error")
                return redirect("")
            if team not in team_names:
                flash("Invalid input for team.", "error")
                return redirect("")
            user, message = create_account(firstname, lastname, email, role, team)
            if message == "exists":
                flash(f"Account with the email {email} already exists.", "error")
            else:
                # If the account doesn't exist then it has automatically been added and an email needs to be sent
                # email is a list since the send emails method takes in a list
                email = [create_email(user)]
                email_links(email)
                if message == "readded":
                    flash(f"User for {firstname} has been re-activated and an email has been sent!", "success")
                elif message == "added":
                    flash(f"User for {firstname} has been created and an email has been sent!", "success")
                else:
                    flash("An error has occurred when creating the account")
        return redirect("")
    else:
        # Only head coaches have access to the edit-roster page
        if current_user.is_coach and current_user.is_head:
            users = User.query.filter(User.password != "not set", User.deleted == False).order_by(User.is_coach.desc(), User.is_head.desc(), User.id).all()
            pending = User.query.filter(User.password == "not set", User.deleted == False).all()
            return render_template('edit_roster.html', users=users, pending=pending, teams=team_names)
        else:
            flash("You do not have permissions to access that page.", "error")
            return redirect(url_for('index'))

# DOWNGRADE MIGRATION BEFORE YOU PUSH TO MAIN!!! -------------------------------------------------------------------------
@app.route('/edit-metrics', methods=["GET", "POST"], strict_slashes=False)
@login_required
def edit_metrics():
    if request.method == "POST":
        # Format of form_identifier: ('c' or 'r' for cox or rower)('e' or 'a' for edit or add)(metric tag, only for editing metrics)
        action = request.form.get("form_identifier")
        name = request.form.get("name")
        if not name: 
            flash("Metrics must have a name.")
            return redirect("")
        desc = request.form.get("desc").strip()

        # Setting who the metric is for
        if action[0] == "r":
            for_cox = False
        else:
            for_cox = True

        # If the action is e for edit then we edit the current empirical metric
        if action[1] == "e":
            tag = action[2:]
            metric = EmpMetrics.query.filter(EmpMetrics.tag == tag, EmpMetrics.team == current_user.team, for_cox=for_cox)

            active = bool(request.form.get("active"))
            metric.name = name
            metric.desc = desc
            metric.active = active

            db.session.commit()


        # If the action is a for add then we create a new empirical metric
        elif action[1] == "a":
            # Need to have temp tag while we create the metric so we know what the id of the new metric is
            tag = "temp"
            new_metric = EmpMetrics(tag=tag, name=name, desc=desc, team=current_user.team, active=True, for_cox=for_cox)
            # Tags are set to be the first character of the metric name and their id
            new_metric.tag = (name[0] + str(new_metric.id))

            db.session.add(new_metric)
            db.session.commit()


    elif request.method == "GET":
        if current_user.is_coach and current_user.is_head:
            team = current_user.team
            # Getting all kinds of metrics seperated into 4 lists. All from current team
            rower_active = EmpMetrics.query.filter(EmpMetrics.for_cox == False, EmpMetrics.active == True, EmpMetrics.team == team).all()
            rower_disabled = EmpMetrics.query.filter(EmpMetrics.for_cox == False, EmpMetrics.active == False, EmpMetrics.team == team).all()
            cox_active = EmpMetrics.query.filter(EmpMetrics.for_cox == True, EmpMetrics.active == True, EmpMetrics.team == team).all()
            cox_disabled = EmpMetrics.query.filter(EmpMetrics.for_cox == True, EmpMetrics.active == False, EmpMetrics.team == team).all()

            return render_template("edit_metrics.html", rower_active=rower_active, rower_disabled=rower_disabled, cox_active=cox_active, cox_disabled=cox_disabled)
        else:
            flash("You do not have permissions to access that page.", "error")
            return redirect(url_for('index'))

if not is_production:
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

