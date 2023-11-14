from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# absolute import, from root directory
# from app.blueprints.auth import routes

# relative route -> 
from . import routes