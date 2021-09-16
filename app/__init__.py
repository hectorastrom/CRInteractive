from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate
from werkzeug.datastructures import auth_property 
from app import config
from imgurpython import ImgurClient

app = Flask(__name__)
client = ImgurClient(client_id=config.client_id, client_secret=config.client_secret)

authorization_url = client.get_auth_url('pin')
app.config['SECRET_KEY'] = config.secretkey

# Coach keys
valid_keys = ["ABC123"]

# Teams
teams = ["Men's Varsity", "Men's U17"]

# To hash do bycrypt.generate_password_hash(password).decode('utf-8')
# To check password do bycrypt.check_password_hash(hashed_password, password)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# flask db init
# flask db migrate -m 'Initial migration'
# flask db upgrade 

migrate = Migrate(app, db)

bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from app import routes
