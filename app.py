from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



app = Flask(__name__)
bcrypt = Bcrypt()
# To hash do bycrypt.generate_password_hash(password).decode('utf-8')
# To check password do bycrypt.check_password_hash(hashed_password, password)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)