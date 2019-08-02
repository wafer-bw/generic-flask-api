"""
Application factory, contains functions for generating the app and
registering extensions, blueprints, error handlers, and initializing
the database
"""

from app import config
from flask import Flask


def create_app(conf_obj_name: str) -> Flask:
    """
    An application factory used to generate the app
    http://flask.pocoo.org/docs/patterns/appfactories/

    Args:
        conf_obj_name (str): Name of the configuration object to use

    Returns:
        Flask: Flask App
    """
    app = Flask(__name__)
    config_import_str = f"app.config.{conf_obj_name}Config"
    app.config.from_object(config_import_str)
    register_blueprints(app)
    register_extensions(app)
    register_error_handlers(app)
    initialize_database(app)
    return app


def register_extensions(app):
    """
    Register all Flask extensions
    """
    from app.utilities.extensions.db import db
    from app.utilities.extensions.cache import cache
    from app.utilities.extensions.migrate import migrate
    db.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)

def register_blueprints(app):
    """
    Register all blueprints
    """
    from app.controllers import blueprints
    [app.register_blueprint(bp, url_prefix=up) for bp, up in blueprints]


def register_error_handlers(app):
    """
    Register all error handlers
    """
    from app.utilities.exceptions import error_handlers
    [app.register_error_handler(hk, hv) for hk, hv in error_handlers.items()]


def initialize_database(app):
    """
    Initialize the database.
    """
    from app.utilities.extensions.db import db
    from app.utilities.database import create_db

    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    create_db(db_uri)

    with app.app_context():
        db.create_all()
