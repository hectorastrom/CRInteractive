from random import randint
from flask import url_for, flash, redirect
from flask.helpers import url_for
from flask_login import current_user
from functools import wraps
from app import db, is_production, teams
from app.models import User
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

# Coach Required Decorator 
def coach_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_coach:
            flash(f'Insufficient permissions', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def convert_from_seconds(total, form):
    """
    Takes in a total amount of seconds from the database and a form to be converted to (split or normal minutes:seconds) and returns teh final string.
    """
    if form == "split":
        split_seconds = total/4
        minutes = int(split_seconds/60)
        seconds = round(split_seconds % 60, 1)
    else:
        minutes = int(total/60)
        seconds = round(total % 60, 1)

    if seconds < 10:
            seconds = "0" + str(seconds)
    return str(minutes) + ":" + str(seconds)

def chooseTeam(input:str) -> str:
    """
    Iterates through the teams dictionary in __init__.py to look for valid team entries.
    Any abbreviations or proper spellings of team from teams will return the proper team.
    A string with the final team name as will be stored in the database is returned.
    """
    input = input.lower().strip()
    # Iterates through possible teams in __init__.py
    for team in teams:
        # If the input is in the list of abbreviations for a team
        # or is equal to the name of the actual team, assign them
        # to that team
        if input in teams[team] or input == team:
            user_team = team
            break
        else: 
            # Unrecognized team names return error, will only happen for command inputs which aren't checked like edit-roster is
            user_team = "error"
    
    return user_team

def chooseRole(user:User, input:str):
    """
    Chooses a role for a user and automatically updates the database to assign them that role.
    Valid Inputs include 'cox' 'coxswain' 'coach' 'hcoach' or anything else which will become a rower.
    """
    input = input.lower().strip()
    if input == "coxswain" or input == "cox":
        user.is_coxswain = True
        user.is_coach = False
        user.is_head = False
    elif input == "coach":
        user.is_coxswain = False
        user.is_coach = True
        user.is_head = False
    elif input == "hcoach":
        user.is_coxswain = False
        user.is_coach = True
        user.is_head = True
    else:
        user.is_coxswain = False
        user.is_coach = False
        user.is_head = False

    db.session.commit()


def create_account(firstname, lastname, email, role, team):
    """
    Takes in a firstname, lastname, email, role (cox, coxswain, hcoach, coach, or anything else => rower), and team (team or abbreviation from teams in __init__.py) and does one of 3 things with:
    1. If the account with that email exists and is active, it returns the exiting user and a message that says it exists.
    2. If the account with that email exists and is disabled, it returns the existing user and reactivates the account and says readded.
    3. If the account does not exist, it creates the account, adds it to the database, and returns that it was added. NO EMAIL IS SENT.
    """
    firstname = firstname.capitalize().strip()
    lastname = lastname.capitalize().strip()
    email = email.lower().strip()
    role = role.lower().strip() 
    # If the team is not valid, then it will end the function there and return error
    team = chooseTeam(team)
    if team == "error":
        print("Invalid team input")
        return (None, "error")
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and not existing_user.deleted:
        return (existing_user, "exists")
    elif existing_user and existing_user.deleted:
        existing_user.deleted = False
        unique_id = randint(10000000, 99999999)
        while User.query.filter_by(uuid=str(unique_id)).first():
            unique_id = randint(10000000, 99999999)
        unique_id = str(unique_id)
        existing_user.uuid = unique_id
        existing_user.firstname = firstname
        existing_user.lastname = lastname
        existing_user.password = "not set"
        # Team is already the result of chooseTeam(team)
        existing_user.team = team
        chooseRole(existing_user, role)
        db.session.commit()
        return(existing_user, "readded")
    else:
        team = team
        unique_id = randint(10000000, 99999999)
        while User.query.filter_by(uuid=str(unique_id)).first():
            unique_id = randint(10000000, 99999999)
        unique_id = str(unique_id)
        user = User(firstname=firstname, lastname=lastname, email=email, team=team, uuid=unique_id)
        chooseRole(user, role)
        db.session.add(user)
        db.session.commit()
        return (user, "added")

def create_email(user:User):
    """
    Takes in a user and creates a single email to be sent to the user.
    """
    EMAIL_ADDRESS = "crinteractivebot@gmail.com"

    msg = EmailMessage()
    msg["Subject"] = f"Your CRInteractive Code is {user.uuid}"
    msg['From'] = formataddr(('CRInteractive', EMAIL_ADDRESS))
    msg['To'] = formataddr((user.firstname, user.email))
    
    msg.set_content(f'Welcome to CRInteractive, {user.firstname}! Your CRInteractive link is https://crinteractive.org/register/{user.uuid}.')

    html = """\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta name="color-scheme" content="light">
        <style type="text/css">
            .nav
            {
                position: absolute;
                top:0px;
                left:0px;
                right:0px;
                background-color: rgb(42, 43, 44);
                width: 100%;
                height: 80px;
                margin:0px !important;
            }
            .svg-container
            {
                height: 100%;
                width: 100%;
                display: flex;
                align-items: center;
            }
            .body-container
            {
                position: absolute;
                top: 80px;
                left: 0px;
                right: 0px;
                padding:15px;
                margin:0px;
                background-color: lightgray;
            }
            body
            {
                margin:0px;
                background-color: lightgray;
                font-family:Verdana, Geneva, Tahoma, sans-serif;
            }
            svg
            {
                height: 30px;
                width: 100%;
                margin: 0 auto;
                display: block;
            }
            .card
            {
                margin-top: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                background-color: white;
                padding: 10px;
                border-radius: 15px;
                max-width: 500px;   
            }
            .container
            {
                padding: 2px 16px;
            }
            a:visited
            {
                color: blue;
            }
            .muted
            {
                color: rgb(128, 128, 128);
            }
        </style>
    </head>
    <body>
        <div class="nav">
            <div class="svg-container">
                <svg width="779.409" height="74.007" viewBox="0 0 779.409 74.007" xmlns="http://www.w3.org/2000/svg"><g id="svgGroup" stroke-linecap="round" fill-rule="evenodd" font-size="9pt" stroke="none" stroke-width="0.25mm" fill="none" style="stroke:rgb(177, 23, 49);stroke-width:0.25mm;fill:rgb(177, 23, 49)"><path d="M 173.205 51.6 L 173.205 44.5 L 160.205 44.5 L 160.205 49.1 A 28.296 28.296 0 0 1 160.044 52.318 C 159.832 54.141 159.395 55.592 158.625 56.447 A 2.473 2.473 0 0 1 156.705 57.3 A 2.565 2.565 0 0 1 154.349 55.843 C 153.664 54.629 153.305 52.608 153.305 49.6 A 11.366 11.366 0 0 0 149.376 41.561 C 147.234 39.479 144.515 37.807 142.005 36.6 A 19.083 19.083 0 0 0 154.012 31.029 C 155.45 29.396 156.525 27.348 157.081 24.794 A 19.692 19.692 0 0 0 157.505 20.6 A 17.663 17.663 0 0 0 155.536 12.18 C 151.609 4.802 142.4 1.7 133.305 1.7 L 76.305 1.7 L 76.305 16.7 L 86.805 16.7 C 88.791 16.7 89.641 17.331 89.907 18.642 A 5.88 5.88 0 0 1 90.005 19.8 L 90.005 52.8 A 11.791 11.791 0 0 1 89.93 54.246 C 89.686 56.193 88.802 57 86.505 57 L 76.305 57 L 76.305 72.1 L 124.705 72.1 L 124.705 57 L 116.005 57 C 113.859 57 112.855 55.762 112.807 52.543 A 16.538 16.538 0 0 1 112.805 52.3 L 112.805 41.7 L 121.405 41.7 A 6.775 6.775 0 0 1 126.936 45.031 C 128.538 47.36 129.366 50.437 129.404 52.644 A 9.159 9.159 0 0 1 129.405 52.8 A 32.866 32.866 0 0 0 130.271 60.767 C 131.961 67.499 136.182 71.49 143.439 72.86 A 34.408 34.408 0 0 0 149.805 73.4 A 44.734 44.734 0 0 0 157.681 72.773 C 168.126 70.897 171.993 64.934 172.95 56.538 A 43.743 43.743 0 0 0 173.205 51.6 Z M 68.505 41.1 L 68.505 40 L 50.605 40 A 38.428 38.428 0 0 1 49.469 49.827 C 47.878 55.749 44.478 59.948 38.438 60.096 A 13.552 13.552 0 0 1 38.105 60.1 A 12.313 12.313 0 0 1 31.599 58.454 C 26.489 55.36 24.505 48.097 24.505 38.3 A 82.198 82.198 0 0 1 24.668 32.944 C 25.174 25.236 27.045 17.324 32.798 14.871 A 10.11 10.11 0 0 1 36.805 14.1 A 10.62 10.62 0 0 1 43.845 16.656 C 46.994 19.305 48.932 23.661 50.124 28.017 A 44.193 44.193 0 0 1 50.405 29.1 A 241.133 241.133 0 0 1 50.578 29.832 C 51.052 31.851 51.605 34.3 51.605 34.3 L 68.505 34.3 L 68.505 1.7 L 51.105 1.7 L 51.105 10.2 A 29.29 29.29 0 0 0 43.218 3.173 C 40.612 1.655 37.696 0.656 34.295 0.232 A 31.414 31.414 0 0 0 30.405 0 A 29.362 29.362 0 0 0 3.451 19.707 A 45.571 45.571 0 0 0 0.005 37.2 A 41.636 41.636 0 0 0 4.243 56.188 C 9.819 67.129 20.677 74 35.505 74 C 56.105 74 68.505 64.5 68.505 41.1 Z M 294.805 72.1 L 294.805 60.7 L 289.205 60.7 C 287.705 60.7 286.305 59.7 286.305 57.6 L 286.305 37.1 A 16.418 16.418 0 0 0 284.924 30.131 C 283.082 26.194 279.322 23.637 273.205 23.505 A 23.25 23.25 0 0 0 272.705 23.5 A 14.627 14.627 0 0 0 263.293 27.657 C 260.713 29.916 258.63 32.655 257.206 34.687 A 93.206 93.206 0 0 0 256.305 36 L 256.305 24.5 L 230.305 24.5 L 230.305 35.7 L 237.405 35.7 C 238.905 35.7 239.305 36.7 239.305 38.6 L 239.305 57.7 A 7.309 7.309 0 0 1 239.235 58.795 C 239.047 60.025 238.439 60.66 236.953 60.698 A 5.671 5.671 0 0 1 236.805 60.7 L 230.305 60.7 L 230.305 72.1 L 260.805 72.1 L 260.805 60.7 L 259.405 60.7 A 2.049 2.049 0 0 1 257.517 59.393 C 257.245 58.819 257.105 58.094 257.105 57.3 L 257.105 42.8 A 7.822 7.822 0 0 1 257.269 41.24 C 257.819 38.541 259.717 35.843 262.228 34.875 A 5.475 5.475 0 0 1 264.205 34.5 A 5.698 5.698 0 0 1 266.126 34.806 C 267.686 35.364 268.605 36.662 268.605 38.5 L 268.605 57.6 A 6.053 6.053 0 0 1 268.514 58.705 C 268.262 60.053 267.493 60.7 266.205 60.7 L 263.305 60.7 L 263.305 72.1 L 294.805 72.1 Z M 521.405 48.5 L 511.905 48.5 L 511.905 56.8 A 12.94 12.94 0 0 1 511.811 58.464 C 511.578 60.244 510.881 61.298 509.378 61.474 A 4.064 4.064 0 0 1 508.905 61.5 A 2.819 2.819 0 0 1 507.323 61.066 C 506.3 60.394 505.805 58.969 505.805 57 L 505.805 36 A 10.117 10.117 0 0 0 499.461 26.513 C 495.459 24.541 490.037 23.771 484.615 23.563 A 89.067 89.067 0 0 0 481.205 23.5 A 37.089 37.089 0 0 0 469.103 25.226 C 464.25 26.939 460.603 30.123 459.651 35.615 A 17.45 17.45 0 0 0 459.405 38.6 L 459.405 42.7 L 476.705 42.7 L 476.705 40.2 C 476.705 37.831 478.282 35.961 481.361 35.647 A 9.309 9.309 0 0 1 482.305 35.6 C 484.457 35.6 486.904 36.118 487.545 38.685 A 5.835 5.835 0 0 1 487.705 40.1 L 487.705 43.6 C 482.976 46.063 474.655 46.973 470.107 47.956 A 35.141 35.141 0 0 0 469.905 48 C 465.363 48.98 458.757 51.705 457.368 58.862 A 14.868 14.868 0 0 0 457.105 61.7 C 457.105 68.2 462.905 73.4 469.405 73.4 A 20.777 20.777 0 0 0 483.233 67.391 A 57.575 57.575 0 0 0 487.105 63.6 L 487.305 63.6 A 10.324 10.324 0 0 0 489.317 68.573 C 491.893 71.881 496.558 73.163 502.182 73.369 A 47.003 47.003 0 0 0 503.905 73.4 A 27.151 27.151 0 0 0 512.998 71.987 C 517.958 70.201 521.405 66.636 521.405 60.8 L 521.405 48.5 Z M 226.405 72.1 L 226.405 57 L 215.905 57 C 213.759 57 212.755 55.762 212.707 52.543 A 16.538 16.538 0 0 1 212.705 52.3 L 212.705 19.6 C 212.705 17.7 213.905 16.7 216.205 16.7 L 226.405 16.7 L 226.405 1.7 L 176.205 1.7 L 176.205 16.7 L 186.705 16.7 C 188.691 16.7 189.541 17.331 189.807 18.642 A 5.88 5.88 0 0 1 189.905 19.8 L 189.905 52.8 A 11.791 11.791 0 0 1 189.83 54.246 C 189.586 56.193 188.702 57 186.405 57 L 176.205 57 L 176.205 72.1 L 226.405 72.1 Z M 340.205 47.8 L 329.205 47.8 L 329.205 57 C 329.205 59.8 327.805 61.7 325.305 61.7 A 5.729 5.729 0 0 1 323.865 61.542 C 322.24 61.118 321.605 59.789 321.605 57 L 321.605 35.7 L 337.205 35.7 L 337.205 24.5 L 321.605 24.5 L 321.605 4.3 L 311.505 4.3 L 311.505 7.5 A 28.235 28.235 0 0 1 311.33 10.64 C 310.552 17.57 307.149 24.5 300.205 24.5 L 294.805 24.5 L 294.805 35.7 L 303.805 35.7 L 303.805 58.8 A 13.472 13.472 0 0 0 305.404 65.411 C 308.457 70.944 315.434 73.334 322.412 73.399 A 31.482 31.482 0 0 0 322.705 73.4 C 331.967 73.4 338.506 69.043 339.919 60.672 A 21.45 21.45 0 0 0 340.205 57.1 L 340.205 47.8 Z M 623.105 47.8 L 612.105 47.8 L 612.105 57 C 612.105 59.8 610.705 61.7 608.205 61.7 A 5.729 5.729 0 0 1 606.765 61.542 C 605.14 61.118 604.505 59.789 604.505 57 L 604.505 35.7 L 620.105 35.7 L 620.105 24.5 L 604.505 24.5 L 604.505 4.3 L 594.405 4.3 L 594.405 7.5 A 28.235 28.235 0 0 1 594.23 10.64 C 593.452 17.57 590.049 24.5 583.105 24.5 L 577.705 24.5 L 577.705 35.7 L 586.705 35.7 L 586.705 58.8 A 13.472 13.472 0 0 0 588.304 65.411 C 591.357 70.944 598.334 73.334 605.312 73.399 A 31.482 31.482 0 0 0 605.605 73.4 C 614.867 73.4 621.406 69.043 622.819 60.672 A 21.45 21.45 0 0 0 623.105 57.1 L 623.105 47.8 Z M 723.105 35.7 L 723.105 24.5 L 698.105 24.5 L 698.105 35.7 L 702.205 35.7 L 697.105 56.3 L 691.205 35.7 L 695.605 35.7 L 695.605 24.5 L 664.705 24.5 L 664.705 35.7 L 673.705 35.7 L 683.205 72.1 L 704.105 72.1 L 715.005 35.7 L 723.105 35.7 Z M 428.405 36 L 428.405 24.5 L 402.305 24.5 L 402.305 35.7 L 409.405 35.7 A 1.557 1.557 0 0 1 410.697 36.492 C 411.109 37.111 411.305 37.97 411.305 38.6 L 411.305 57.8 C 411.305 59.5 410.805 60.7 408.805 60.7 L 402.305 60.7 L 402.305 72.1 L 437.405 72.1 L 437.405 60.7 L 431.405 60.7 A 2.327 2.327 0 0 1 430.371 60.483 C 429.61 60.111 429.214 59.278 429.125 58.125 A 6.849 6.849 0 0 1 429.105 57.6 L 429.105 48.3 C 429.105 44.5 431.205 34.7 434.705 34.7 A 3.198 3.198 0 0 1 435.905 34.907 C 437 35.347 437.473 36.464 437.581 38.037 A 11.22 11.22 0 0 1 437.605 38.8 L 437.605 45.6 L 453.605 45.6 L 453.605 39.8 C 453.605 33.501 452.075 26.513 445.531 24.863 A 12.753 12.753 0 0 0 442.405 24.5 A 11.153 11.153 0 0 0 437.036 25.876 C 432.611 28.266 429.882 33.195 428.405 36 Z M 575.405 50.6 L 562.305 50.6 C 561.79 56.354 560.611 60.411 556.046 61.443 A 11.53 11.53 0 0 1 553.505 61.7 C 548.605 61.7 545.505 59 545.505 52.8 L 545.505 41.6 C 545.505 39.052 546.317 36.95 547.759 35.76 A 4.678 4.678 0 0 1 550.805 34.7 C 554.805 34.7 556.205 37.3 556.205 40.3 L 556.205 44.5 L 572.105 44.5 L 572.105 40.1 C 572.105 29.74 564.025 23.663 552.09 23.503 A 36.205 36.205 0 0 0 551.605 23.5 C 537.473 23.5 526.981 33.264 525.814 46.771 A 29.383 29.383 0 0 0 525.705 49.3 A 24.015 24.015 0 0 0 546.023 72.929 A 28.42 28.42 0 0 0 551.205 73.4 C 567.205 73.4 573.505 64.4 575.105 54.2 A 10.098 10.098 0 0 0 575.153 53.877 C 575.321 52.617 575.405 50.6 575.405 50.6 Z M 397.705 54.8 L 385.805 54.8 A 13.561 13.561 0 0 1 381.036 61.155 C 379.869 61.919 378.496 62.439 376.868 62.625 A 12.025 12.025 0 0 1 375.505 62.7 A 9.391 9.391 0 0 1 370.456 61.401 C 368.251 60.022 366.795 57.514 366.409 53.724 A 20.942 20.942 0 0 1 366.305 51.6 L 398.205 51.6 A 36.775 36.775 0 0 0 396.364 39.585 C 393.334 30.816 386.66 25.25 377.017 23.849 A 34.86 34.86 0 0 0 372.005 23.5 A 26.754 26.754 0 0 0 355.294 29.089 C 350.062 33.23 346.652 39.422 346.246 46.807 A 27.204 27.204 0 0 0 346.205 48.3 A 25.064 25.064 0 0 0 368.702 73.184 A 28.343 28.343 0 0 0 372.205 73.4 A 28.415 28.415 0 0 0 384.245 70.888 A 25.061 25.061 0 0 0 397.705 54.8 Z M 778.905 54.8 L 767.005 54.8 A 13.561 13.561 0 0 1 762.236 61.155 C 761.069 61.919 759.696 62.439 758.068 62.625 A 12.025 12.025 0 0 1 756.705 62.7 A 9.391 9.391 0 0 1 751.656 61.401 C 749.451 60.022 747.995 57.514 747.609 53.724 A 20.942 20.942 0 0 1 747.505 51.6 L 779.405 51.6 A 36.775 36.775 0 0 0 777.564 39.585 C 774.534 30.816 767.86 25.25 758.217 23.849 A 34.86 34.86 0 0 0 753.205 23.5 A 26.754 26.754 0 0 0 736.494 29.089 C 731.262 33.23 727.852 39.422 727.446 46.807 A 27.204 27.204 0 0 0 727.405 48.3 A 25.064 25.064 0 0 0 749.902 73.184 A 28.343 28.343 0 0 0 753.405 73.4 A 28.415 28.415 0 0 0 765.445 70.888 A 25.061 25.061 0 0 0 778.905 54.8 Z M 662.905 72.1 L 662.905 60.7 L 656.205 60.7 A 2.585 2.585 0 0 1 655.16 60.506 C 654.469 60.202 654.054 59.536 653.938 58.46 A 6.214 6.214 0 0 1 653.905 57.8 L 653.905 24.5 L 627.005 24.5 L 627.005 35.7 L 633.005 35.7 A 6.835 6.835 0 0 1 634.097 35.776 C 635.625 36.025 636.105 36.93 636.105 39 L 636.105 57.7 C 636.105 59.949 635.579 60.617 633.62 60.693 A 10.82 10.82 0 0 1 633.205 60.7 L 627.005 60.7 L 627.005 72.1 L 662.905 72.1 Z M 653.705 16.3 L 653.705 1.7 L 635.405 1.7 L 635.405 16.3 L 653.705 16.3 Z M 112.805 32.2 L 112.805 16.7 L 123.905 16.7 A 21.945 21.945 0 0 1 127.092 16.907 C 130.91 17.471 132.77 19.208 133.137 22.351 A 10.775 10.775 0 0 1 133.205 23.6 A 10.824 10.824 0 0 1 132.448 27.856 C 131.31 30.518 128.786 32.2 124.205 32.2 L 112.805 32.2 Z M 487.805 48.5 L 487.805 50.8 C 487.805 57.1 484.305 62.7 479.805 62.7 A 3.842 3.842 0 0 1 476.244 60.245 A 6.471 6.471 0 0 1 475.705 57.6 A 5.821 5.821 0 0 1 478.082 53.15 A 14.169 14.169 0 0 1 481.805 51 A 106.253 106.253 0 0 0 482.466 50.742 C 484.931 49.769 487.14 48.796 487.68 48.556 A 43.315 43.315 0 0 0 487.805 48.5 Z M 379.805 42.6 L 367.005 42.6 A 17.839 17.839 0 0 1 367.236 39.573 C 367.848 36.042 369.72 34.2 373.305 34.2 A 7.387 7.387 0 0 1 376.064 34.674 C 378.299 35.569 379.477 37.719 379.746 41.035 A 19.422 19.422 0 0 1 379.805 42.6 Z M 761.005 42.6 L 748.205 42.6 A 17.839 17.839 0 0 1 748.436 39.573 C 749.048 36.042 750.92 34.2 754.505 34.2 A 7.387 7.387 0 0 1 757.264 34.674 C 759.499 35.569 760.677 37.719 760.946 41.035 A 19.422 19.422 0 0 1 761.005 42.6 Z" vector-effect="non-scaling-stroke"/></g></svg>   
            </div>
        </div>
        <div class="body-container">
            <center>
                <div class="card">
                    <div class="container">
                        <h2>Welcome, """ + user.firstname + """!</h2>
                        <p>You've been invited to use <span style="color:rgb(177, 23, 49)">CRInteractive</span>. Use the following link to finish creating your account.</p>  
                        <p><a href="https://www.crinteractive.org/register/""" + user.uuid + """">www.crinteractive.org/register/""" + user.uuid + """</a></p>
                        <small class="muted">This link is unique to you. Do not share it with anyone else. Impersonation is a violation of the <strong style="color:black;">CRI Code of Conduct</strong>.</small>
                    </div>
                </div> 
            </center>
        </div>
    </body>
</html>
"""

    msg.add_alternative(html, subtype='html')
    return msg

def email_links(messages):
    """
    Takes in a LIST of emails and iterates through them, sending the emails using the information in the email object.
    """
    if is_production:
        EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
        EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    else: 
        from app.config import email_address, email_password
        EMAIL_ADDRESS = email_address
        EMAIL_PASSWORD = email_password
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        for message in messages:
            smtp.send_message(message)
            print("Email sent to", message['To'])

class MetricText():
    def __init__(self, tag, name, desc=""):
        self.tag = tag
        self.name = name
        self.desc = desc
        
    def __repr__(self) -> str:
        return f'*Tag: {self.tag}, Name: {self.name}, Description: {self.desc}*'


class MetricObj():
    def __init__(self, tag:str, name:str, desc:str, coach_rating:int, coach_importance:int, user_rating:int, view_allowed:bool, has_set:bool, has_update:bool, note:str) -> None:
        self.tag = tag
        self.name = name
        self.desc = desc
        self.note = note
        self.coach_rating = coach_rating
        self.coach_importance = coach_importance
        self.user_rating = user_rating
        self.view_allowed = view_allowed
        self.has_set = has_set
        self.has_update = has_update

    def __repr__(self) -> str:
        return f"""Metric {self.tag}
        Name: {self.name}
        Note: '{self.note}'
        CoachRating: {self.coach_rating}
        CoachImp: {self.coach_importance}
        UserRating: {self.user_rating}"""
