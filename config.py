import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SITE_NAME = 'wages'
    GITHUB_USERNAME = 'daisutao'
    EMAIL = 'daisutao@163.com'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f43hrt53et53'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BOOTSTRAP_SERVE_LOCAL = True
