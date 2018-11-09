from flask import Flask
from config import Config
from wages.extensions import *
from wages.models import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    debugtoolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    from wages.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from wages.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from wages.staff import bp as staff_bp
    app.register_blueprint(staff_bp)

    from wages.error import bp as error_bp
    app.register_blueprint(error_bp)

    return app
