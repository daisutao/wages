from flask import Blueprint

bp = Blueprint('errors', __name__)

from wages.errors import handlers