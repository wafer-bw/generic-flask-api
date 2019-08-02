"""
All blueprints of routes which need to be accessible must be here.
They will be registered when the application is started.

Includes a controller for a basic index page.
"""

from typing import Tuple
from flask import Blueprint, Response

from app.controllers.generic import generic_bp
from app.utilities.extensions.cache import cache

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
@cache.cached()
def index() -> Tuple[Response, int]:
    """
    Responds with basic 'Hello World'

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """
    from app.utilities.responder import Responder
    responder = Responder()
    return responder.succeed(msg="Hello World!")

blueprints = [
    (index_bp, "/"),
    (generic_bp, "/"),
]
