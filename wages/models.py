from wages.extensions import db, login
from werkzeug import security
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5


class Dept(db.Model):
    __tablename__ = 'depts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True, nullable=False)

    def __repr__(self):
        return f'<Dept {self.name}>'


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    employee = db.Column(db.String(10), index=True, unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    hire_date = db.Column(db.DateTime)
    skill_grade = db.Column(db.String(10))  # 职级
    bank_account = db.Column(db.String(20))  # 个人账号
    dept_id = db.Column(db.Integer, db.ForeignKey('depts.id'))
    department = db.relationship('Dept')

    base_skills = db.Column(db.Float)   # 基本职能
    performance = db.Column(db.Float)   # 基本业绩
    job_ability = db.Column(db.Float)   # 业绩能力
    housing_subsidy = db.Column(db.Float)   # 住房补
    leader_subsidy = db.Column(db.Float)    # 职位补
    fixed_overtime = db.Column(db.Float)    # 固定加班费
    traffic_subsidy = db.Column(db.Float)   # 交通补
    housing_fund = db.Column(db.Float)      # 住房公积金
    trade_union = db.Column(db.Float)       # 工会会费

    def __repr__(self):
        return f'<User {self.employee}>'

    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def check_password(self, password):
        return security.check_password_hash(self.password_hash, password)

    @property
    def is_administrator(self):
        return self.employee == 'admin'

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Daily(db.Model):
    __tablename__ = 'daily'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(10), index=True, nullable=False)

    working = db.Column(db.Integer)  # 工作 unit: hour
    leave01 = db.Column(db.Integer)  # 事假 unit: hour
    leave02 = db.Column(db.Integer)  # 病假 unit: hour
    leave03 = db.Column(db.Integer)  # 丧假 unit: hour
    leave04 = db.Column(db.Integer)  # 婚假 unit: hour
    leave05 = db.Column(db.Integer)  # 产假 unit: hour
    leave06 = db.Column(db.Integer)  # 年休假 unit: hour
    leave07 = db.Column(db.Integer)  # 工作假 unit: hour
    leave08 = db.Column(db.Integer)  # 陪产假 unit: hour
    leave09 = db.Column(db.Integer)  # 流产假 unit: hour
    leave10 = db.Column(db.Integer)  # 路程假 unit: hour
    leave11 = db.Column(db.Integer)  # 其它假 unit: hour
    come_late = db.Column(db.Integer)  # 迟到 unit: minute
    left_early = db.Column(db.Integer)  # 早退 unit: minute
    skip_work = db.Column(db.Integer)  # 旷工 unit: hour

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
