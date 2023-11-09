from flask import Flask
from config import ConFig


app = Flask(__name__)
app.config.from_object(ConFig)

from app import routes