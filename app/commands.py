from re import U
import click
from flask import url_for
from flask.cli import with_appcontext
from random import randint
from app import db, is_production
from app.models import EmpMetrics, Entry, EntryNote, User, Metric, Twok, Fivek
from app.helpers import chooseRole, create_account, create_email, email_links, chooseTeam

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    print("Tables Created.")


@click.command(name='drop_tables')
@with_appcontext
def drop_tables():
    users = User.query.all()
    print(f"Are you sure you want to drop tables for all {len(users)} users? ")
    response = input("Y/N: ")
    if response.lower() == "y":
        db.drop_all()
    else: 
        print("Task exited.")

# Run with a command like flask add_user test test test@example.com rower "Men's Varsity"
@click.command(name='add_user')
@click.argument("firstname")
@click.argument("lastname")
@click.argument("email")
@click.argument("role")
@click.argument("team")
@with_appcontext
def add_user(firstname, lastname, email, role, team):
    user, message = create_account(firstname, lastname, email, role, team)
    if message == "added":
        print("Added", user, "to database.")
    elif message == "readded":
        print("Re-activated", user, "in database.")
    elif message == "exists":
        print("User with email", email, "already exists:", user)
    else:
        print("Error occured while trying to add user.")



@click.command(name='remove_user')
@click.argument("email")
@with_appcontext
def remove_user(email):
    user = User.query.filter_by(email=email).first()
    if user:
        print("Are you sure you want to permanently remove this user and all their data:", user, "?")
        response = input("Y/N: ")
        if response.lower() == "y":
            all_metrics = Metric.query.filter_by(user_id = user.id).all()
            for metric in all_metrics:
                db.session.delete(metric)
            user_twoks = Twok.query.filter_by(user_id = user.id).all()
            for twok in user_twoks:
                db.session.delete(twok)
            user_fiveks = Fivek.query.filter_by(user_id = user.id).all()
            for fivek in user_fiveks:
                db.session.delete(fivek)
            db.session.delete(user)
            db.session.commit()
            print("User with email", email, "and all their data was permanentely deleted.")
        else:
            print("Task exited.")
    else: 
        print("No user with email", email, "found.")

@click.command(name='query_user')
@click.argument("input")
@with_appcontext
def query_user(input):
    """
    Accepts either user emails or id's as input and prints information regrading the chosen user.
    """
    is_email = False
    if '@' in input:
        is_email = True
    if is_email:
        user = User.query.filter(User.email.ilike(input)).first()
    elif input.isnumeric(): 
        user = User.query.get(int(input))
    if not user and is_email:
        print("User with", input, "email does not exist.")
    elif not user and not is_email:
        print(f"User with id {input} does not exist.")
    else:
        if user.password == "not set":
            status = "Uninitialized"
        else:
            status = "Initialized"
        if user.deleted:
            status += ", Deleted"
        print(f"Status: {status}")
        print(f"First name: {user.firstname}")
        print(f"Last name: {user.lastname}")
        print(f"Email: {user.email}")
        print(f"Team: {user.team}")
        print(f"Side: {user.side}")
        print(f"UUID: {user.uuid}")
        if user.is_head:
            role = "Head Coach"
        elif user.is_coach:
            role = "Coach"
        elif user.is_coxswain:
            role = "Coxswain"
        else:
            role="Rower"
        print(f"Role: {role}")
        print(f"Date Created: {user.date_created}")
        if not is_production:
            print(f"Link to Register Page: 127.0.0.1:5000/register/{user.uuid}")

@click.command(name='edit_user')
@click.argument("email")
@with_appcontext
def edit_user(email):
    user = User.query.filter(User.email == email).first()
    if not user: 
        print(f"User with email {email} not found.")
        return 1
    print(f"What element would you like to edit for {email}?")
    print("1. Name")
    print("2. Role")
    print("3. Team")
    choice = input()
    while not choice.isdigit() or int(choice) not in [1,2,3]:
        choice = input("Invalid input. Try again: ")
    choice = int(choice)
    if choice == 1:
        print(f"Current name: {user.firstname} {user.lastname}")
        name = input(f"What is their name (case-sensitive, first and lastname seperated by space): ")
        user.firstname = name[:name.index(" ")]
        user.lastname = name[name.index(" ") + 1:]
        db.session.commit()
        print(f"Updated name to be {user.firstname} {user.lastname}")

    if choice == 2:
        role = input(f"What is {user.firstname}'s role: ")
        chooseRole(user, role)
        print(f"User now set with the following variables: is_cox: {user.is_coxswain}, is_coach:{user.is_coach}, is_head:{user.is_head}")

    if choice == 3:
        print(f"{user.firstname}'s current team: {user.team}")
        team = input("What is the correct team: ")
        user.team = chooseTeam(team)
        db.session.commit()
        print(f"User's team updated to be {user.team}.")

@click.command(name='send_email')
@click.argument("email")
@with_appcontext
def send_email(email):
    user = User.query.filter(User.email.ilike(email)).first()
    if user:
        messages = [create_email(user)]
        email_links(messages)
    else:
        print(f"No user with {email} found. Try adding the user first.")

@click.command(name='send_emails')
@with_appcontext
def send_emails():
    import csv

    db.create_all()
    messages = []

    with open("app/static/rowers.csv", "r") as file:
        csv_reader = csv.reader(file)
        # Skips the titles of each column
        next(csv_reader) 
        row_number = 0
        has_error = False
        for row in csv_reader:
            row_number += 1
            firstname = row[0].strip()
            lastname = row[1].strip()
            email = row[2].lower().strip()
            role = row[3]
            team = row[4]
            user, message = create_account(firstname, lastname, email, role, team)
            if message == "exists":
                print("User with email", email, "already exists in the database with code " + user.uuid + ". Ignored.")
            elif message == "error":
                print(f"Invalid team input in row {row_number}. User with email {email} not added to database and no email sent.")
                has_error = True
            else:
                if message == "added":
                    print("User with firstname:", firstname, "lastname:", lastname, "email:", email, "UUID:", user.uuid, "added to database.")
                elif message == "readded":
                    print("User with firstname:", firstname, "lastname:", lastname, "email:", email, "UUID:", user.uuid, "re-activated in database.")
                msg = create_email(user)
                messages.append(msg)      

    if not has_error:
        print("\nFinished iteration through csv with no problems.")
    else:
        print("\nFinished iteration through csv with one or more errors. Look above.")
    if(messages):
        print(f"Sending {len(messages)} emails now...\n")
        email_links(messages)
    else:
        print("0 new users to email.\n")
    print("Finished 'send_emails' command.")

@click.command(name='create_empmetric')
@click.argument("tag")
@click.argument("name")
@click.argument("team")
@with_appcontext
def create_empmetric(tag, name, team):
    """
    Function just for testing purposes until a dedicated interface is developed for creating empirical metrics. Takes in tag, name and team.
    """
    team = chooseTeam(team.lower().strip())
    if team == "error":
        print("Invalid team input.")
        return 1
    existing_metric = EmpMetrics.query.filter(EmpMetrics.tag==tag, EmpMetrics.team==team).first()
    if existing_metric:
        print(f"A metric on {team} with tag {tag} already exists.")
    else:
        new_metric = EmpMetrics(tag=tag, name=name, desc="Test description", team=team)
        db.session.add(new_metric)
        db.session.commit()
        print(f"Added {new_metric}to emperical metric list")

@click.command(name='clear_empmetrics')
@with_appcontext
def clear_empmetrics():
    current_empmetrics = EmpMetrics.query.all()
    numMetrics = len(current_empmetrics)
    response = input(f"Are you sure you would like to clear all {numMetrics} Metrics PERMANENTELY: ").lower()
    if response == "yes" or response == "y":
        EmpMetrics.query.delete()
        db.session.commit()
        print("Metrics successfully deleted.")
    else:
        print("Metrics were not deleted.")
    current_entries = Entry.query.all()
    numEntries = len(current_empmetrics)
    response = input(f"Would you also like to clear all {numEntries} Entries (otherwise existing Entries with correlate with new Emp Metrics): ")
    if response == "yes" or response == "y":
        Entry.query.delete()
        EntryNote.query.delete()
        db.session.commit()
        print("Entries have been deleted.")
    else:
        print("Entries were not deleted.")

@click.command(name='print_usertable')
@click.argument("team")
@with_appcontext
def print_usertable(team):
    team = chooseTeam(team.lower().strip())
    if team == "error":
        print("Invalid team input")
        return 1
    users = User.query.filter_by(team=team).all()
    for user in users:
        if user.password != "not set":
            status="Registered"
        else:
            status="Unregistered"

        if user.is_head:
            role = "Head Coach"
        elif user.is_coach:
            role = "Coach"
        elif user.is_coxswain:
            role = "Coxswain"
        else: 
            role = "Rower"

        print(f'ID {user.id}: {status} {role} with Name: "{user.firstname} {user.lastname}", Email: "{user.email}", Created: {user.date_created}, Accessed: {user.last_accessed}')