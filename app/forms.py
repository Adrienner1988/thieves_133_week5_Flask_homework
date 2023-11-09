from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('Email Address: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class SearchForm(FlaskForm):
    search = StringField('Search Pokémon by Name or National Pokédex Number:', validators=[DataRequired()])
    search_btn = SubmitField('Search')