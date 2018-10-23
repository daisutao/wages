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

    from wages.main import bp as main_bp
    app.register_blueprint(main_bp)

    from wages.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from wages.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
