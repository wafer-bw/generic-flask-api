"""
All Models are listed here for import or dynamic/generic use
"""

from app.models.users import Users
from app.models.fruits import Fruits

models = {
    "users": Users,
    "fruits": Fruits,
}