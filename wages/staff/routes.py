from wages.staff import bp

from flask import redirect, render_template, request, url_for, current_app, flash, g
from flask_login import current_user, login_required
from wages.models import User, db


@bp.route('/user/<string:employee>')
@login_required
def user(employee):
    user = User.query.filter_by(employee=employee).first_or_404()
    return render_template('user.html', user=user)
