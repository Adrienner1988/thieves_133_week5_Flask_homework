from flask import Blueprint

team = Blueprint('team', __name__, template_folder='team_templates')

from . import team