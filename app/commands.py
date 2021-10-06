import click
import os
from flask.cli import with_appcontext
from random import randint
from app import db, is_production
from app.models import User, Metric, Twok, Fivek
from app.helpers import create_account, create_email, email_links

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()


@click.command(name='drop_tables')
@with_appcontext
def drop_tables():
    db.drop_all()

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
    else:
        print("User with email", email, "already exists:", user)



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


@click.command(name='send_emails')
@with_appcontext
def send_emails():
    import csv

    db.create_all()
    messages = []

    with open("app/static/rowers.csv", "r") as file:
        if is_production:
            EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
            EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        else: 
            EMAIL_ADDRESS = "crinteractivebot@gmail.com"
            EMAIL_PASSWORD = "2hourdrive&will" 

        csv_reader = csv.reader(file)
        # Skips the titles of each column
        next(csv_reader) 
        row_number = 0
        for row in csv_reader:
            row_number += 1
            firstname = row[0].capitalize().strip()
            lastname = row[1].capitalize().strip()
            email = row[2].lower().strip()
            role = row[3]
            if row[4].lower().strip() == "mv":
                team = "Men's Varsity"
            elif row[4].lower().strip() == "l" or row[4].lower().strip() == "fl":
                team = "Fall Launchpad"
            else:
                print(f"ERROR: Unrecognized team value in row {row_number}: {row[3]}. Defaulted to Fall Launchpad.")
                team = "Fall Launchpad"
            user, message = create_account(firstname, lastname, email, role, team)
            if message == "exists":
                print("User with email", email, "already exists in the database with code " + user.uuid + ". Ignored.")
            else:
                print("User with firstname:", firstname, "lastname:", lastname, "email:", email, "UUID:", user.uuid, "added to database.")
                msg = create_email(user)
                messages.append(msg)      

    print("\nFinished iteration through csv. Sending emails now.\n")
    email_links(messages)
    print("\nFinished 'send_emails' command.")

