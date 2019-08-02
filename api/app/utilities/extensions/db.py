"""
Flask Sqlalchemy Database Extension
https://flask-sqlalchemy.palletsprojects.com/en/2.x/

This must be registered to the app within app/factory.py

Note: flask_sqlalchemy will remove the session at the end of
the request context. This means we don't need to worry about starting
and stopping database sessions on our own.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
