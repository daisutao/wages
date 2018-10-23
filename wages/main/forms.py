from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadForm(FlaskForm):
    sheet = FileField('考勤文件',
                      validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], '只能上传考勤Excel文件！')])
    submit = SubmitField('上传')

