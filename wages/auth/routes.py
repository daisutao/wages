from flask import render_template, redirect, url_for, flash, request, abort
from wages.auth.forms import LoginForm, RegisterForm
from wages.auth import bp
from flask_login import current_user, login_user, logout_user
from wages.models import User
from wages.extensions import db


@bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.wages'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(employee=form.employee.data).first_or_404()
        login_user(user)
        if user.is_administrator:
            url = url_for('admin.wages')
        else:
            url = url_for('staff.wages')
        return redirect(request.args.get('next') or url)
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('auth/login'))
