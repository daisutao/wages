from wages.admin import bp

from flask import redirect, render_template, request, url_for, current_app, flash, g
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from wages.admin.forms import UploadForm
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


def plus(data, x, a, b):
    if data[x] != 0:
        data[a] += data[x] * 0.5
        data[b] += data[x] * 0.5
    return data


@bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.sheet.data
        # filename = secure_filename(f.filename)
        try:
            df = pd.read_excel(f, usecols='B:D,M:V,Y,AA:AB')
            group1 = df.groupby(['工号', '姓名'])['调休时数', '迟到分钟', '早退分钟', '旷工天数',
                                              '平时加班', '休日加班', '假日加班'].sum()
            group2 = df.groupby(['工号', '姓名', '请假类别'])['请假天数'].sum()
            group2 = group2.unstack(level=2, fill_value=0)

            for col in group2.columns:
                mix = col.split(',')
                if len(mix) > 1:
                    group2 = group2.apply(plus, axis=1, args=(col, mix[0], mix[1]))
                    group2.drop(col, axis=1, inplace=True)

            new_df = pd.concat([group1, group2], axis=1)
            new_df.fillna(0, inplace=True)

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
            return render_template('admin/wages.html', df=new_df)

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
        # return redirect(url_for('admin.wages'))


@bp.route('/wages', methods=['GET', 'POST'])
@login_required
def wages():
    return render_template('admin/wages.html')


# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user = User(employee=form.employee.data, username=form.username.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('注册成功！', 'success')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/register.html', form=form)