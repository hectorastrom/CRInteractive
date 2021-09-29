from app import db

print(db.User.query.all())

"""
Read in each user in the csv from google sheets. If the user exists already, do nothing. Otherwise
create a new user for them setting the firstname, lastname, email, and unique id which will be sent to
their email for them to sign up. The unique id is a 8 digit code that will be UNIQUE and will also query 
the User database for other codes like that before assigning it to a user. Once each user is created
it will be easy to create a route in routes.py that queries the database at route /create-account/<UUID>/
for a user with that UUID and allows them to enter their password before creating the account. 

"""