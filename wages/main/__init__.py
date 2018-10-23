from flask import Blueprint

bp = Blueprint('main', __name__)

from wages.main import routes