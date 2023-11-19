from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

#creating instance of database
db = SQLAlchemy()


#bridge table
user_poke = db.Table(
    'user_poke',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')), # user table, id attribute
    db.Column('poke_id', db.Integer, db.ForeignKey('poke.id'))  # poke table, id attribute
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    Pokemon = db.relationship('Poke', secondary=user_poke, backref='user')

    def __init__(self, full_name, email, password):
        self.full_name = full_name
        self.email = email
        self.password = generate_password_hash(password)


# building an instance of a pokemon
class Poke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ability = db.Column(db.String, nullable=False)
    attack_stat = db.Column(db.Integer, nullable=False)
    hp_stat = db.Column(db.Integer, nullable=False)
    defense_stat = db.Column(db.Integer, nullable=False)
    sprite = db.Column(db.String, nullable=False)

    def __init__(self, name, ability, attack_stat, hp_stat, defense_stat, sprite, poke_added):
       self.name = name
       self.ability = ability
       self.attack_stat = attack_stat
       self.hp_stat = hp_stat
       self.defense_stat = defense_stat
       self.sprite = sprite
       self.poke_added = poke_added
    



