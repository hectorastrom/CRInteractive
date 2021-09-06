from flask.app import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import validate_arguments
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, SelectField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from datetime import date
from wtforms.fields.html5 import DateField
from flask_login import current_user
from app import valid_keys

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
    
    def validate_firstname(self, firstname):
        if not firstname.data.isalpha():
            raise ValidationError('First name contains characters which are not letters. Please try a different name.')

    def validate_lastname(self, lastname):
        if not lastname.data.isalpha():
            raise ValidationError('Last name contains characters which are not letters. Please try a different last name.')

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

    def validate_minutes(self, field):
        if field.data > 59:
            raise ValidationError('Minutes cannot exceed a value of 59.')
    
    def validate_seconds(self, field):
        if field.data > 59.9:
            raise ValidationError('Seconds cannot exceed a value of 59.9.')

    def validate_date(self, field):
        if field.data > date.today():
            raise ValidationError('Date cannot be later than today\'s date.')

class CoachRegistrationForm(FlaskForm):
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
    coach_key = StringField('Coach Key', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Please choose a different email.')
    
    def validate_firstname(self, firstname):
        if not firstname.data.isalpha():
            raise ValidationError('First name contains characters which are not letters. Please try a different name.')

    def validate_lastname(self, lastname):
        if not lastname.data.isalpha():
            raise ValidationError('Last name contains characters which are not letters. Please try a different last name.')
    
    def validate_coach_key(self, coach_key):
        if not coach_key.data.isalnum():
            raise ValidationError('Coach key contains characters which aren\'t alphanumeric. Please try another key.')
        if coach_key.data not in valid_keys:
            raise ValidationError('This is not a valid coach key. Please try another key.')

