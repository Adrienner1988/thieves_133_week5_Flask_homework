from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField('Enter Pokémon Name or National Pokédex Number:', validators=[DataRequired()])
    search_btn = SubmitField('Search')
