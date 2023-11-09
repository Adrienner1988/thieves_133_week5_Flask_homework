from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, SearchField, StringField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('Email Address: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class SearchForm(FlaskForm):
    search = SearchField('Search Pokémon by Name or National Pokédex Number:', validators=[DataRequired()])
    search_btn = SubmitField('Search')

class SignUp(FlaskForm):
    full_name = StringField('Full Name: ', validators=[DataRequired()])
    email = EmailField('Email Address: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Login')