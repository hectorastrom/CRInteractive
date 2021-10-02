from app import db
from app.models import User
import csv

print(User.query.all())
db.session.commit()

with open("rowers.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    row_number = 0
    for row in csv_reader:
        row_number += 1
        firstname = row[0].capitalize()
        lastname = row[1].capitalize()
        email = row[2].lower()
        if row[3].lower() == "mv":
            team = "Men's Varsity"
        elif row[3].lower() == "l":
            team = "Launchpad"
        else:
            print(f"ERROR: Unrecognized team value in row {row_number}: {row[3]}.")
            quit()
        if row[4].lower() == "coxswain":
            is_coxswain = True
        else: 
            is_coxswain == False

        if row[4].lower() == "coach":
            is_coach = True
        else:
            is_coach = False
        
            

"""
Read in each user in the csv from google sheets. If the user exists already, do nothing. Otherwise
create a new user for them setting the firstname, lastname, email, and unique id which will be sent to
their email for them to sign up. The unique id is a 8 digit code that will be UNIQUE and will also query 
the User database for other codes like that before assigning it to a user. Once each user is created
it will be easy to create a route in routes.py that queries the database at route /create-account/<UUID>/
for a user with that UUID and allows them to enter their password before creating the account. 

"""