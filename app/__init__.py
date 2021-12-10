from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate
from werkzeug.datastructures import auth_property 
import os
#from app import config
#from imgurpython import ImgurClient

app = Flask(__name__)
is_production = os.getenv("production")
if is_production.lower() == "true":
    is_production = True
else:
    is_production = False
#client = ImgurClient(client_id=config.client_id, client_secret=config.client_secret)

#authorization_url = client.get_auth_url('pin')
if is_production:
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
else: 
    app.config['SECRET_KEY'] = 'alksdjfasdffikluwenfdsfuje'

# Teams and abbreviations, abbreviations must be lowercase
mvabrv = ["mv", "vm"]
flabrv = ["fl", "l"]
vwabrv = ["gv", "vw"]
teams = {"Men's Varsity": mvabrv, "Fall Launchpad": flabrv, "Varsity Women":vwabrv}

# To hash do bycrypt.generate_password_hash(password).decode('utf-8')
# To check password do bycrypt.check_password_hash(hashed_password, password)
if is_production:
    uri = os.getenv("DATABASE_URL") 
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# flask db init
# flask db migrate -m 'Initial migration'
# flask db upgrade 

migrate = Migrate(app, db, compare_type=True, render_as_batch=True)

bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# # Need to import from helpers before adding all commands since they rely on these commands
# from app.helpers import create_email, create_account, send_emails

from app.commands import create_tables, drop_tables, send_emails, remove_user, add_user, query_user, send_email, create_empmetric, clear_empmetrics

app.cli.add_command(create_tables)
app.cli.add_command(drop_tables)
app.cli.add_command(send_emails)
app.cli.add_command(send_email)
app.cli.add_command(remove_user)
app.cli.add_command(add_user)
app.cli.add_command(query_user)
app.cli.add_command(create_empmetric)
app.cli.add_command(clear_empmetrics)



from app import routes
