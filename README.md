# CRInteractive: Coach-Athlete Transparency

### CRInteractive is a Flask Website created by Hector Astrom and Albert Astrom for their rowing team CRI. Their coach wanted a way to quickly and visually convey how different competencies of each athelete on the team appear in the coach's eyes. The website intends to generate discussion between the coach and athlete as well as inform the athlete on what they need to work on.

#  
All accounts for CRInteractive are managed for the users by the head coach of each team. Initially, account information is stored in a spreadsheet that is read and creates accounts for all users. New users will receive emails with a register link to finish setting up their account. Here, they are able to set their password. This password is hashed and stored in the database so that only the person with the account is ever able to log in. Future user additions are handled by the head coach in the edit roster portal where details can be adjusted for users. 
  
Once logged in, users are greeted with the screen of their profile where they will spend most of their time. Here is where they will find all the metrics the coaches have shared with them. Once a metric is shared with them, they are able to indicate their competency of that metric before being able to view what the coach said for it. This creates genuine ratings from both parties so that they can be compared and discussed.
  
In the future, athletes will be able to share their condition: how they slept last night, how busy they've been, if they have any illness, etc. This will allow coaches to better understand the attitudes of the athletes.

# Making Changes On Production Server

## Steps to upgrade the database on the live server: 
1. Create new branch on VSCode and **set is_production to *False***

1. Edit models.py for database change

1. Run `flask db migrate -m "change description"`

1. Run `flask db upgrade` and `python run.py` to test change.

1. If everything works as expected, **set is_production to *True*** and merge branch with main

1. Do this at night and set the CRInteractive Heroku server into maintenance mode. 

1. Push changes and wait for deployment to Heroku to finish

1. Once in Heroku run flask db upgrade

1. If an error message appears saying "Missing revision with id ..." then head back to VSCode main branch and run `flask db revision --rev-id ...`

1. Push the change with the new revision

1. Run `flask db upgrade` on Heroku again

1. Take server out of maintenance mode

1. Your server should be live and the changes complete. 


For more information, refer to here:

https://flask-migrate.readthedocs.io/en/latest/

https://stackoverflow.com/questions/47656071/commanderror-cant-locate-revision-identified-by-when-migrating-using-fla
