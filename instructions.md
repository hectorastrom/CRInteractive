# CRInteractive: Coach-Athlete Transparency

### CRInteractive is a Flask Website created by Hector Astrom and Albert Astrom for their rowing team CRI. Their coach wanted a way to quickly and visually convey how different competencies of each athelete on the team appear in the coach's eyes. The website intends to generate discussion between the coach and athlete as well as inform the athlete on what they need to work on.

#  
All accounts for CRInteractive are managed for the users by the head coach of each team. Initially, account information is stored in a spreadsheet that is read and creates accounts for all users. New users will receive emails with a register link to finish setting up their account. Here, they are able to set their password. This password is hashed and stored in the database so that only the person with the account is ever able to log in. Future user additions are handled by the head coach in the edit roster portal where details can be adjusted for users. 
  
Once logged in, users are greeted with the screen of their profile where they will spend most of their time. Here is where they will find all the metrics the coaches have shared with them. Once a metric is shared with them, they are able to indicate their competency of that metric before being able to view what the coach said for it. This creates genuine ratings from both parties so that they can be compared and discussed.
  
In the future, athletes will be able to share their condition: how they slept last night, how busy they've been, if they have any illness, etc. This will allow coaches to better understand the attitudes of the athletes.

# Commands Reference
  
### `flask create_tables`
- Creates all tables in database. Creates new tables in database if new tables are added.
### `flask drop_tables`
- Drops all tables in database (users, workouts, and metrics) after prompting the user to confirm they want to drop the tables.
### `flask add_user 'firstname' 'lastname' 'email' 'role' 'team'`
- Using the provided inputs, add_user creates a user if they don't already exist. If they already exist and are not deleted, it will print the information of the existing user. If they already exist and are deleted it'll reactive the user and print their information. If the user does not exist it will add them BUT WILL NOT SEND AN EMAIL TO THEM. 
- The valid inputs for role are "cox", "coxswain", "coach", "hcoach". Any other input for role will become a rower
- The valid inputs for team are "men's varsity", "mv", "l", "fl", "fall launchpad". Multiple word teams must be put in "quotes" as input.
- All inputs are defaulted to lowercase and are stripped for easier inputs.
### `flask edit_user 'email'`
- Finds user with specified email to change either their name, role, or team.
### `flask remove_user 'email'`
- Removes user with the email provided, asking for confirmation before DELETING (not setting to deleted) the user.
### `flask query_user 'email'`
- Prints information for the user with the email provided.
### `flask send_email 'email'`
- Creates and sends and email to the user with the email provided.
### `flask send_emails`
- Opens and reads the rowers.csv file in the static folder and creates accounts for and emails all users not already in the database. Each user added is printed and a messages if an email was sent to them is printed. If a user is already in the database then they are ignored.
### `flask print_usertable 'team'`
- Takes in a team name (abbreviated or not) and prints a table with all users on that team. Each user's id, registration status, name, email, and registration date is printed.


# Making Changes On Production Server
#### Ideally, database changes should be done at night and with the CRInteractive Heroku server into maintenance mode. 
Commands to preface:
  - `flask db migrate` creates a migration file, a python file with instructions for flask migrate on how to upgrade and downgrade the database
  - `flask db upgrade` upgrades the database to the migration file after the one it is currently on.
  - `flask db current` tells you the current migration file you are currently on
  - `flask db stamp head` skips all migrations up to the head and just stamps the head (most recent) migration as the one that is supposedly "active for the database". Try to avoid this but it can also solve some weird issues.
  
  Important Note: Don't **EVER** run flask db migrate on the production server. This will generate a migration file that only exists on the ephemeral file system of Heroku and cannot be accessed elsewhere (troubleshooting below in case you ever do).
  
  ## Steps to upgrade the database on the live server: 
1. Create new branch on VSCode with relevant name for database change

1. Edit models.py for database change

1. Run `flask db migrate -m "change description"`

1. Run `flask db upgrade` and `python run.py` in VSCode to test change before upgrading database on live server. 

1. If all works as expected, put Heroku server into maintenance mode to prepare the change

1. Push the change, and merge branch with main

1. Once the built in finished in Heroku, run `flask db upgrade`

1. Take server out of maintenance mode

1. Your server should be live and the changes complete. 

Potential Errors: 
1. If an error message appears saying "Missing revision with id ..." then head back to VSCode main branch and run `flask db revision --rev-id ...`. This error occurs from having run `flask db migrate` on the production server, which creates a migration file only on the production server (not in repo).

    * Push the change with the new revision
    * Run `flask db upgrade` on Heroku again

1. If an error occurs during `flask db upgrade`, that means only part of the upgrade has gone through: Lots of good information in https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite 

    * Figure out what part of the upgrade went through (by looking at schema or maybe order of upgrades)
    * Clear upgrade() function in migration file
    * Edit downgrade() function so that the only thing reversed is what was changed (top bullet)
    * Run `flask db downgrade` to downgrade that migration
    * Delete failed migration file and figure out the issue.

1. If an upgrade version is not recognized (no relevant message printed from `flask db upgrade`), then this could be because the database was pushed to main in an upgraded state (not the same migration version as production server is) which makes the production server think it has already upgraded even though it's still on a lower version. If this does happen (which I'm not sure why it would since alembic version in local db is different from production but I think it's happened before), then go into VSCode and downgrade the database to match the production migration file, and then push this new version of the database. Then you can probably run `flask db upgrade` on production and it'll recognize the new changes. 


For more information, refer to here:

* https://flask-migrate.readthedocs.io/en/latest/

* Deleting migration files:
  https://github.com/miguelgrinberg/Flask-Migrate/issues/333

* https://stackoverflow.com/questions/47656071/commanderror-cant-locate-revision-identified-by-when-migrating-using-fla

For problems involving partial upgrades^ (especially for string length changes) refer to this:
https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite
  
# Changing Metrics
  
Metrics are now changed by the head coach and are specific to each team. 

# Email Issues

If there is an issue sending emails (error saying that you don't have access to the gmail account) there are a few things you must do:
1. Check if Less Secure App Access in on in Google. To find out, go to Account in Google > Security > Scroll down to Less Secure App Access and switch to On. This can turn off randomly.
2. See if there is a popup to say that the device trying to sign in is you. If there isn't, head to Account > Security > Recent Security Activity and then click on the relevant sign in attempt to say it was you.
3. While signed in as crinteractivebot@gmail.com head to https://accounts.google.com/b/0/DisplayUnlockCaptcha and click Allow. This basically just allows the next sign in to access the account. 

**More permanently we should switch to using Google Gmail API with more information here: https://stackoverflow.com/a/54715276**
