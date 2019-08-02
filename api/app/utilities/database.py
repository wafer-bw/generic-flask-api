"""
Database helpers and Mixins
"""

from sqlalchemy.inspection import inspect
from app.utilities.extensions.db import db
from app.utilities.helpers import is_jsonable

# Aliases
Column = db.Column
ForeignKey = db.ForeignKey
Integer = db.Integer
String = db.String


def create_db(db_uri: str):
    """
    Create the database if it does not exist

    Args:
        db_uri (str): URI of DB to create
    """
    from sqlalchemy_utils import create_database, database_exists
    if not database_exists(db_uri):
        create_database(db_uri)


def drop_db(db_uri: str):
    """
    Drop the database if it exists

    Args:
        db_uri (str): URI of DB to drop
    """
    from sqlalchemy_utils import drop_database, database_exists
    if database_exists(db_uri):
        drop_database(db_uri)


class CRUDMixin(object):
    """
    Mixin that adds methods for create, read, update, and
    delete operations
    """


    @classmethod
    def create(cls, **kwargs):
        """
        Create a new record then save it to the database.
        """
        instance = cls(**kwargs)
        return instance.save()


    def save(self, commit:bool=True) -> object:
        """
        Save record to database

        Args:
            commit (bool, optional): Commit or not. Defaults to True.

        Returns:
            object: Created self instance (regardless of Commit or not)
        """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self


    @property
    def as_dict(self) -> dict:
        """
        Return dict version of self instance

        Returns:
            dict: This instance as a dict instead of a class object
        """
        obj = {}
        for c in inspect(self).mapper.column_attrs:
            val = getattr(self, c.key)
            if is_jsonable(val):
                obj.update({c.key: val})
        return obj


    def update(self, commit:bool=True, **kwargs) -> bool:
        """
        Update specified fields of a record

        Args:
            commit (bool, optional): Commit or not. Defaults to True.

        Returns:
            bool: True if operation was commited, False otherwise
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self


    def delete(self, commit:bool=True) -> bool:
        """
        Remove the record from the database

        Args:
            commit (bool, optional): Commit or not. Defaults to True.

        Returns:
            bool: True if operation was commited, False otherwise
        """
        db.session.delete(self)
        if commit:
            db.session.commit()
        return commit


class Model(CRUDMixin, db.Model):
    """
    Base db model class that also includes CRUD methods.
    """
    __abstract__ = True
