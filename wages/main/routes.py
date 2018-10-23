from wages.main import bp
import os
from flask import redirect, render_template, request, url_for, current_app, flash, g
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from wages.main.forms import UploadForm
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


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.sheet.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            current_app.instance_path, filename
        ))
        flash('上传成功！', 'success')
        return redirect(url_for('main.wages'))
    return render_template('index.html', form=form)


@bp.route('/wages')
@login_required
def wages():
    return render_template('wages.html')


@bp.route('/user/<string:employee>')
@login_required
def user(employee):
    user = User.query.filter_by(employee=employee).first_or_404()
    return render_template('user.html', user=user)
