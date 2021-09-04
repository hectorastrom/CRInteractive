from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
with open('app/static/secretkey.txt', 'r') as f:
    secretkey = f.readline()
    app.config['SECRET_KEY'] = secretkey
bcrypt = Bcrypt()
# To hash do bycrypt.generate_password_hash(password).decode('utf-8')
# To check password do bycrypt.check_password_hash(hashed_password, password)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from app import routes