from flask.app import Flask
from flask_wtf import FlaskForm
from werkzeug.utils import validate_arguments
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from datetime import date
from wtforms.fields.html5 import DateField

import email_validator

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', 
                            validators=[DataRequired(), Length(min=2, max=30)])
    lastname = StringField('Last Name', 
                            validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Please choose a different email.')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class TwokForm(FlaskForm):
    minutes = IntegerField('Minutes', 
                          validators=[DataRequired()], render_kw={"placeholder": "6"})
    seconds = FloatField('Seconds', 
                          validators=[DataRequired()], render_kw={"placeholder": "42.5"})
    date = DateField('Date Completed', format='%Y-%m-%d', 
                    validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def validate_seconds(self, field):
        if field.data > 60:
            raise ValidationError('Cannot exceed 60 seconds')

    def validate_date(self, field):
        if field.data > date.today():
            raise ValidationError('Date cannot be later than today\'s date.')
