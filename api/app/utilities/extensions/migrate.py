"""
Flask Migrate Extension
https://flask-migrate.readthedocs.io/en/latest/

This must be registered to the app within app/utilities/application_factory.py
"""

from flask_migrate import Migrate

migrate = Migrate()
