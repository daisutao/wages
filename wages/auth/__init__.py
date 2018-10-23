from flask import Blueprint

bp = Blueprint('auth', __name__)

from wages.auth import routes