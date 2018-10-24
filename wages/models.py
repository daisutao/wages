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
