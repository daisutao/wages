from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from wtforms.validators import DataRequired, EqualTo, ValidationError
from wages.models import Dept, User


class LoginForm(FlaskForm):
    employee = StringField('工号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录',
                         render_kw={"class": "col-md-4 offset-md-4 btn btn-primary btn-block mb-2"})

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(employee=self.employee.data).first()
        if not self.user:
            self.employee.errors.append('该用户不存在！')
            return False

        if not self.user.check_password(password=self.password.data):
            self.password.errors.append('密码错误！')
            return False
        return True


def query_factory():
    return Dept.query


class RegisterForm(FlaskForm):
    employee = StringField('工号', validators=[DataRequired()])
    username = StringField('姓名', validators=[DataRequired()])
    # deptlist = QuerySelectField('部门', validators=[DataRequired()],
    #                             query_factory=query_factory, get_label='name')
    password = PasswordField('密码', validators=[DataRequired()])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(employee=self.employee.data).first()
        if self.user:
            self.employee.errors.append('该用户已存在！')
            return False

        return True
