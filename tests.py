import os
import pandas as pd
from sqlalchemy import create_engine, types, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from werkzeug import security

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))
df = pd.read_excel('工资201809.xlsx', sheet_name='工资计算模板', header=7,
                   usecols='C,F:H,K,M:P,R:T,Y,AD,AJ', dtype={'工号': str, '个人账号': str})

df.columns = ['hire_date', "employee", "username", 'department', 'skill_grade', "bank_account",
              "base_skills", "performance", "job_ability", "housing_subsidy", "leader_subsidy",
              "fixed_overtime", "traffic_subsidy", "housing_fund", "trade_union"]

df = df[df.employee != "nan"]
df.dropna(subset=['hire_date'], inplace=True)
df.replace(['管理部管理课', '管理部'], '管理课', inplace=True)

BaseModel = declarative_base()


class Dept(BaseModel):
    __tablename__ = 'depts'
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(20), unique=True)

    def __repr__(self):
        return self.name


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(types.Integer, primary_key=True)
    employee = Column(types.String(10), index=True, unique=True, nullable=False)
    username = Column(types.String(20), nullable=False)
    password_hash = Column(types.String(128))
    last_seen = Column(types.DateTime, default=datetime.utcnow)

    hire_date = Column(types.DateTime)
    skill_grade = Column(types.String(10))  # 职级
    bank_account = Column(types.String(20))  # 个人账号
    dept_id = Column(types.Integer, ForeignKey('depts.id'))
    department = relationship('Dept')

    base_skills = Column(types.Float)  # 基本职能
    performance = Column(types.Float)  # 基本业绩
    job_ability = Column(types.Float)  # 业绩能力
    housing_subsidy = Column(types.Float)  # 住房补
    leader_subsidy = Column(types.Float)  # 职位补
    fixed_overtime = Column(types.Float)  # 固定加班费
    traffic_subsidy = Column(types.Float)  # 交通补
    housing_fund = Column(types.Float)  # 住房公积金
    trade_union = Column(types.Float)  # 工会会费


BaseModel.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

for item in df.groupby('department')['employee'].count().index:
    dept = Dept(name=item)
    # 添加到session:
    session.add(dept)
# 提交即保存到数据库:
session.commit()

# 添加 admin
user = User(employee='admin', username='管理员', password_hash=security.generate_password_hash('888888'))
session.add(user)
# 添加 staff
for index, row in df.iterrows():
    department = session.query(Dept).filter_by(name=row.department).first()
    user = User(employee=row.employee, username=row.username, password_hash=security.generate_password_hash('123456'),
                hire_date=row.hire_date, skill_grade=row.skill_grade, bank_account=row.bank_account,
                dept_id=department.id, base_skills=row.base_skills, performance=row.performance,
                job_ability=row.job_ability,
                housing_subsidy=row.housing_subsidy, leader_subsidy=row.leader_subsidy,
                fixed_overtime=row.fixed_overtime,
                traffic_subsidy=row.traffic_subsidy, housing_fund=row.housing_fund, trade_union=row.trade_union)
    session.add(user)
# 提交即保存到数据库:
session.commit()

# 关闭session:
session.close()
