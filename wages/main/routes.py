from wages.main import bp
import os
from flask import redirect, render_template, request, url_for, current_app, flash, g
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from wages.main.forms import UploadForm
from wages.models import User, db
from datetime import datetime
import pandas as pd


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
        try:
            df = pd.read_excel(f, usecols='B:D,M:V,Y,AA:AB')
            group = df.groupby(['工号', '姓名'])['调休时数', '产假天数', '请假天数', '请假类别', '迟到分钟', '早退分钟', '旷工天数',
                                             '平时加班', '休日加班', '假日加班'].sum()
            # for index, row in df.iterrows():
            #     line = db.session.query(SpcLine).filter_by(line_no=row['A']).first()
            #     if line:
            #         data = db.session.query(SpcData).filter_by(spc_line_id=line.id, spc_key=row['B']).first()
            #         if not data:
            #             data = SpcData(spc_key=row['B'], spc_val=row['C'], spc_line_id=line.id)
            #             db.session.add(data)
            #         else:
            #             data.spc_val = row['C']
            #         db.session.commit()
            flash('上传成功！', 'success')
            return render_template('wages.html', df=group)

            # flash(_('The csv file uploaded successfully!'), 'info')
            # return redirect(request.referrer)
        except Exception as e:
            flash('Error saving data, try again', str(e))
            return redirect(request.referrer)

        # f.save(os.path.join(
        #     current_app.instance_path, filename
        # ))
        # flash('上传成功！', 'success')
        # return render_template('wages.html', df=group)
        # return redirect(url_for('main.wages'))
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
