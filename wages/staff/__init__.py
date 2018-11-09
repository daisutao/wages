from flask import Blueprint

bp = Blueprint('staff', __name__)

from wages.staff import routes