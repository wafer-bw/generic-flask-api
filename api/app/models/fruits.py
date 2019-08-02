"""
Generic Model
"""

from app.utilities.extensions.db import db
from app.utilities.extensions.cache import cache
from app.utilities.helpers import pagination_dict
from app.utilities.database import Model, Column, String, Integer, ForeignKey


class Fruits(Model):
    """
    Generic model
    As long as a controller/route/view that is registered with the Flask
    App imports this model the Database will automatically include the table
    for this model.

    Args:
        **kwargs:
            name (str): Name of item
    """

    __tablename__ = __qualname__.lower()

    # Keeping this here so we can see how to add foreign keys
    # fk = ForeignKey("owner.id", onupdate="NO ACTION", ondelete="CASCADE")

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(33), nullable=False, unique=True)
    # owner_id = Column(Integer, fk)


    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)


    def __repr__(self) -> str:
        """
        Represent instance as a string.

        Returns:
            str: Representation of instance as a string
        """
        return f"<{self.__tablename__.title()} ({self.name})>"
