from wages.main import bp
from flask import render_template, current_app, g
from flask_login import current_user, login_required
from wages.models import User, db
from datetime import datetime


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.title = current_app.config['SITE_NAME']
    g.github_username = current_app.config['GITHUB_USERNAME']
    g.email = current_app.config['EMAIL']


@bp.route('/')
def index():
    return render_template('index.html')


@login_required
@bp.route('/user/<string:employee>')
def user(employee):
    user = User.query.filter_by(employee=employee).first_or_404()
    return render_template('user.html', user=user)
