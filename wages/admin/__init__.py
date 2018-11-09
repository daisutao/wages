from flask import Blueprint

bp = Blueprint('admin', __name__)

from wages.admin import routes