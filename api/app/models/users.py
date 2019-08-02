"""
Users Model
"""

from datetime import datetime as dt
from flask import current_app
from app.utilities.extensions.db import db
from app.utilities.extensions.bcrypt import bcrypt
from app.utilities.database import Model, Column, String, Integer, ForeignKey


class Users(Model):
    """
    User table model
    As long as a controller/route/view that is registered with the Flask
    App imports this model the Database will automatically include the table
    for this model.

    Args:
        **kwargs:
            email (str): Email address of user
            password (bytes): Password of user
            admin (bool): Whether or not the user is an admin
    """

    __tablename__ = __qualname__.lower()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = Column(db.String(128), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.utcnow)


    def __init__(self, email, password=None, admin=False, **kwargs):
        db.Model.__init__(self, email=email, admin=admin, **kwargs)
        if password:
            self.set_password(str(password))
        else:
            self.password = None


    def set_password(self, password: str):
        """
        Set user password hash
        
        Args:
            password (str): Entered user password
        """
        self.password = bcrypt.generate_password_hash(password)


    def check_password(self, value: str) -> bool:
        """
        Check if passed password value is correct

        Args:
            value (str): Password value to check

        Returns:
            bool: True if password is correct, False otherwise
        """
        return bcrypt.check_password_hash(self.password, str(value))


    def __repr__(self) -> str:
        """
        Represent instance as a string.
        
        Returns:
            str: Representation of instance as a string
        """
        return f"<{self.__tablename__.title()} ({self.email})>"
