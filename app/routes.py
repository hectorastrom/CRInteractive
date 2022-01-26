from flask import render_template, url_for, flash, redirect, request
from flask.ctx import copy_current_request_context
from flask.helpers import url_for
from werkzeug.datastructures import ContentRange
from app import app, db, bcrypt, teams, is_production
from app.forms import RegistrationForm, LoginForm, TwokForm
from app.models import User, Twok, Fivek, Metric, EmpMetrics, Entry, EntryNote
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date, datetime
from random import randint
from app.helpers import MetricObj, convert_from_seconds, coach_required, create_account, create_email, email_links, chooseRole, accessed
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
            flash(f"Incorrect credentials. Please check email and password.", "error")
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
        user.deleted = False
        db.session.commit()
        login_user(user, remember=True)
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('index'))
    else:
        if current_user.is_authenticated:
            flash("You may not register an account while logged in.", "error")
            logout_user()
            return redirect(url_for("login"))
        if not user:
            flash("Invalid Registration Code.", "error")
            return redirect(url_for("search_code"))
        elif user and user.password != "not set":
            flash("Account has already been created.", "error")
            return redirect(url_for("login"))
        else:
            return render_template("register.html", form=form, user=user)



@app.route('/settings', methods=["GET", "POST"], strict_slashes=False)
@login_required
def settings():
    accessed()
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
    accessed()
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
                updated_metric = EmpMetrics.query.filter(EmpMetrics.tag == request.form.get("form_identifier"), EmpMetrics.team == current_user.team).first()
                updated_entry = Entry.query.filter(Entry.empmetric_id == updated_metric.id, Entry.user_id == user.id).order_by(Entry.id.desc()).first()
                # If nothing was found, which could happen if the user inspects element, then it won't continue
                if not updated_entry:
                    flash("Problem submitting form. Please try again.", "error")
                    return redirect('')
                user_rating = int(request.form.get(f"{updated_metric.tag}_user_rating"))
                if not user_rating or user_rating < 0 or user_rating > 100:
                    flash("Invalid value for user rating", "error")
                    return redirect('')
                updated_entry.user_rating = user_rating
                db.session.commit()
                flash(f"You may now view coach's rating for {updated_metric.name}.", "success")
                return redirect('')
        elif current_user.is_coach:
            if request.form.get("form_identifier") == "silence":
                user.pinged = False
                db.session.commit()
                flash("Request has been silenced.", "success")
                return redirect('')
            else:
                reference_metric = EmpMetrics.query.filter(EmpMetrics.tag == request.form.get("form_identifier"), EmpMetrics.team == current_user.team).first()
                coach_rating = int(request.form.get(f"{reference_metric.tag}_coach_rating"))
                if not coach_rating or coach_rating < 0 or coach_rating > 100:
                    flash("Invalid value for coach rating", "error")
                    return redirect('')
                coach_importance = int(request.form.get(f"{reference_metric.tag}_coach_importance"))
                if not coach_importance or coach_importance < 0 or coach_importance > 10:
                    flash("Invalid value for coach importance", "error")
                    return redirect('')
                view_allowed = bool(request.form.get(f"{reference_metric.tag}_view_allowed"))
                new_entry = Entry(
                    coach_rating=coach_rating, 
                    coach_importance=coach_importance, 
                    view_allowed=view_allowed, 
                    coach_id=current_user.id,
                    empmetric_id=reference_metric.id, 
                    user_id=user.id
                    )
                db.session.add(new_entry)
                db.session.commit()

                note = request.form.get(f"{reference_metric.tag}_coach_notes").strip()
                if "`" in note:
                    flash(f"Note for {reference_metric.name} may not contain the character `.", "error")
                    return redirect(request.url)
                if note:
                    new_note = EntryNote(content=note, entry_id=new_entry.id)
                    db.session.add(new_note)
                
                db.session.commit()
                flash(f"Updated {reference_metric.name} for {user.firstname}.", "success")
                return redirect('')
    # If it's a GET request
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
        

        active_metrics = EmpMetrics.query.filter(EmpMetrics.team == current_user.team, EmpMetrics.for_cox == user.is_coxswain, EmpMetrics.active == True).all()
        # Entries will store all the entries for the CURRENT empirical metrics
        entries = []
        for metric in active_metrics:
            # Ordered by descending id so we get the most recent entry with the filters 
            # Could also be done with descending datetime but that seems more intensive in my mind
            entry = Entry.query.filter(Entry.empmetric_id == metric.id, Entry.user_id == user.id).order_by(Entry.id.desc()).first()
            if entry:
                if not entry.user_rating:
                    user_rating = 50
                elif entry.user_rating == entry.coach_rating and entry.user_rating > 0:
                    user_rating = entry.user_rating - 1
                else:
                    user_rating = entry.user_rating
                date = entry.date_created.strftime('%A, %B %e, %Y')
                note = EntryNote.query.filter_by(entry_id = entry.id).first()
                coach = User.query.get(entry.coach_id)
                coach_name = f"{coach.firstname} {coach.lastname}"
                entries.append(
                    MetricObj(
                        tag=metric.tag,
                        name=metric.name,
                        desc=metric.desc,
                        coach_rating=entry.coach_rating,
                        coach_importance=entry.coach_importance,
                        user_rating=user_rating,
                        view_allowed=entry.view_allowed,
                        # Has_set will almost always be true, except for the first time
                        # when there is no entry where it will be false
                        has_set=True,
                        # If there's no user_rating then there's an update (for the rower), otherwise there's an update
                        # since there is no rower response
                        has_update=bool(not entry.user_rating),
                        # Need this crazy stuff since entry.note is a backref that returns a list of all EntryNotes
                        # with the id of the Entry and the list is interpreted as a string and printed as [] when it should
                        # just be blank
                        note="" if not note else note.content,
                        date=date,
                        coach_name = coach_name
                    )
                )
            # Only coaches will add metrics to the list of "entries" to be displayed
            # since they need to see the metrics on each profile even if they're not created
            elif not entry and current_user.is_coach:
                entries.append(
                    MetricObj(
                        tag=metric.tag,
                        name=metric.name,
                        desc=metric.desc,
                        coach_rating=50,
                        coach_importance=5,
                        user_rating=50,
                        # view_allowed is defaulted to be whatever the coach has their view prefs as
                        view_allowed=current_user.default_on,
                        has_set=False,
                        has_update=True,
                        note="",
                        date="",
                        coach_name=""
                    )
                )
        if current_user.is_coach:
            return render_template('coach_profile.html', image_file = image_file, user=user, entries=entries, twok=twok, fivek=fivek)
        else:
            entries.sort(key=lambda x:x.coach_importance, reverse=True)
            return render_template('user_profile.html', image_file = image_file, user=user, entries=entries, twok=twok, fivek=fivek)


@app.route('/2k', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def upload_twok():
    accessed()
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
    accessed()
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
    accessed()
    # Coaches renders roster
    if current_user.is_coach:
        users = User.query.filter(User.team==current_user.team, User.is_coach == False, User.deleted == False).order_by(User.pinged.desc(), User.lastname).all()
        # Athletes is a dictionary of all users on the coach's roster and their status of if all metrics are set.
        athletes = {}
        for user in users:
            for_coxswain = False
            if user.is_coxswain:
                for_coxswain = True
            # Status for a user is default set and set to incomplete if there
            # is a single empirical metric without an entry for the user
            status = "set"
            active_metrics = EmpMetrics.query.filter(EmpMetrics.team == current_user.team, EmpMetrics.active == True, EmpMetrics.for_cox == user.is_coxswain).all()
            for metric in active_metrics:
                if not Entry.query.filter(Entry.empmetric_id == metric.id, Entry.user_id == user.id).first():
                    status = "incomplete"
                    break
            athletes[user] = status
        # This turns athletes into a list of tuples sorted by incomplete or not
        athletes = sorted(athletes.items(), key=lambda x: x[1])
        has_rower_metrics = bool(EmpMetrics.query.filter(EmpMetrics.team == current_user.team, EmpMetrics.for_cox == False, EmpMetrics.active == True).all())
        has_cox_metrics = bool(EmpMetrics.query.filter(EmpMetrics.team == current_user.team, EmpMetrics.for_cox == True, EmpMetrics.active == True).all())
        return render_template('roster.html', athletes=athletes, has_cox_metrics = has_cox_metrics, has_rower_metrics = has_rower_metrics)
    # Rowers render team
    else:
        users = User.query.filter(User.team==current_user.team, User.is_coach == False, User.deleted == False).order_by(User.lastname).all()
        return render_template("team.html", users=users)

@app.route('/edit-roster', methods=["GET", "POST"], strict_slashes=False)
@login_required
def edit_roster():
    accessed()
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
            elif form_identifier[:5] == "email":
                email = [create_email(user)]
                try:
                    email_links(email)
                except:
                    flash(f"Error sending email to {user.email}, contact developer", "error")
                    print("Email was not sent, likely because less secure app access if off")
                    return redirect("")
                flash(f"Resent a registration email to {user.email}", "success")
        else: # For creating a user
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
            users = User.query.filter(User.password != "not set", User.deleted == False, User.team == current_user.team).order_by(User.is_coach.desc(), User.is_head.desc(), User.id).all()
            pending = User.query.filter(User.password == "not set", User.deleted == False, User.team == current_user.team).all()
            return render_template('edit_roster.html', users=users, pending=pending, teams=team_names)
        else:
            flash("You do not have permissions to access that page.", "error")
            return redirect(url_for('index'))

@app.route('/edit-metrics', methods=["GET", "POST"], strict_slashes=False)
@login_required
def edit_metrics():
    accessed()
    if request.method == "POST":
        # Format of form_identifier: ('c' or 'r' for cox or rower)('e' or 'a' for edit or add)[metric tag, only for editing metrics]
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
            metric = EmpMetrics.query.filter(EmpMetrics.tag == tag, EmpMetrics.team == current_user.team, EmpMetrics.for_cox==for_cox).first()
            active = True
            if request.form.get("active") == "False":
                active = False
            
            metric.name = name
            metric.desc = desc
            metric.active = active

            db.session.commit()
        # If the action is a for add then we create a new empirical metric
        elif action[1] == "a":
            # Need to have temp tag while we create the metric so we know what the id of the new metric is
            tag = "temp"
            new_metric = EmpMetrics(tag=tag, name=name, desc=desc, team=current_user.team, active=True, for_cox=for_cox)
            db.session.add(new_metric)
            db.session.commit()
            # Tags are set to be the first character of the metric name and their id
            new_metric.tag = (name[0] + str(new_metric.id))
            db.session.commit()
        elif action[1] == "r":
            tag = action[2:]
            target_metric = EmpMetrics.query.filter(EmpMetrics.tag==tag, EmpMetrics.name==name).first
            db.session.remove(target_metric)
            db.session.commit()
            

        return redirect('')
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

@app.route('/contact', strict_slashes=False)
def contact():
    return render_template('contact.html')

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

