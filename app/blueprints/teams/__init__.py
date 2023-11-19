from flask import Blueprint

teams = Blueprint('teams', __name__, template_folder='teams_templates')

from . import routes