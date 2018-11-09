from flask import Blueprint

bp = Blueprint('error', __name__)

from wages.error import handlers