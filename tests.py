import pandas as pd
from sqlalchemy import create_engine
import os

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))
df = pd.read_excel('C:/工资201809.xlsx', sheet_name='工资计算模板', header=7,
                   usecols='F:H,K,M:P,R:T,Y,AD,AJ', dtype={'工号': str, '个人账号': str})
df = df[df['工号'] != "nan"]

df.columns = ["employee", "username", 'department', 'rank' "account", "base_funtion", "basic_performance",
              "solid_result", "housing_allowance", "position_allowance",
              "fixed_overtime", "traffic_allowance", "provident_fund", "union_due"]

# 1. 保存到users表
df.to_sql('salarys', index=False, con=engine, if_exists='append')
# 2. 保存到wages表
df.to_sql('salarys', index=False, con=engine, if_exists='append')
