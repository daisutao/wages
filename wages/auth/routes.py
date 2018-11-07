from flask import render_template, redirect, url_for, flash, request, abort
from wages.auth.forms import LoginForm, RegisterForm
from wages.auth import bp
from flask_login import current_user, login_user, logout_user
from wages.models import User
from wages.extensions import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.wages'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(employee=form.employee.data).first()
        login_user(user)
        return redirect(request.args.get('next') or url_for('main.wages'))
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(employee=form.employee.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('main.index'))
