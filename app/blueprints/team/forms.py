from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class TeamForm(FlaskForm):
    name = StringField('Pokémon: ')
    ability = StringField('Ability: ')
    attack_stat = StringField('Attack Stat: ')
    hp_stat = StringField('HP Stat: ')
    defense_stat = StringField('Defense Stat: ')
    sprite = StringField('Sprite ')
    submit_btn = SubmitField('Select Pokémon')
  