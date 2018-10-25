from wages.extensions import db, login
from werkzeug import security
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5


class Dept(db.Model):
    __tablename__ = 'depts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True, nullable=False)
    user = db.relationship('User', backref='user')

    def __repr__(self):
        return f'<Dept {self.name}>'


class Salary(db.Model):
    __tablename__ = 'salarys'

    id = db.Column(db.Integer, primary_key=True)                                   #id
    employee = db.Column(db.String(10), index=True, unique=True, nullable=False)   #工号
    account = db.Column(db.String(20), nullable=True)             #个人账号
    base_funtion = db.Column(db.Float)        #基本职能
    basic_performance = db.Column(db.Float)   #基本业绩
    solid_result = db.Column(db.Float)        #业绩能力
    housing_allowance = db.Column(db.Float)   #住房补贴
    position_allowance = db.Column(db.Float)  #职位补
    fixed_overtime = db.Column(db.Float)      #固定加班费
    traffic_allowance = db.Column(db.Float)   #交通补
    provident_fund = db.Column(db.Float)      #公积金
    union_due = db.Column(db.Float)           #工会会费

    def __repr__(self):
        return f'<Salary {self.employee}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    employee = db.Column(db.String(10), index=True, unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    dept_id = db.Column(db.Integer, db.ForeignKey('depts.id'))

    def __repr__(self):
        return f'<User {self.employee}>'

    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)
    
    def check_password(self, password):
        return security.check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
