"""
Exception Handlers

http://flask.pocoo.org/docs/1.0/patterns/errorpages/
http://flask.pocoo.org/docs/1.0/patterns/apierrors/
http://werkzeug.palletsprojects.com/en/0.15.x/exceptions/

Exceptions need to be registered via flask app.register_error_handler()
"""

from typing import Tuple
from flask import Response
from sqlalchemy.exc import OperationalError
from redis.exceptions import ConnectionError
from app.utilities.responder import Responder


def generic_exception_handler(exc: Exception) -> Tuple[Response, int]:
    """
    A handler for any raised uncaught exceptions

    Args:
        exc (Exception): A raised uncaught exception

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """
    return Responder().fail(msg="Something went wrong", http_code=500)


def redis_conn_handler(exc: ConnectionError) -> Tuple[Response, int]:
    """
    A handler for redis.exceptions.ConnectionError

    Args:
        exc (ConnectionError): Redis connection error

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """
    return Responder().fail(msg="Cache error", http_code=500)


def sqlalchemy_conn_handler(exc: OperationalError) -> Tuple[Response, int]:
    """
    A handler for sqlalchemy.exc.OperationalError

    Args:
        exc (OperationalError): SQL Alchemy operational error

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """
    return Responder().fail(msg="Database error", http_code=500)


def generic_http_handler(http_exc: Exception) -> Tuple[Response, int]:
    """
    A handler for HTTP exceptions via werkzeug.exceptions

    Args:
        http_exc (Exception): werkzeug.exceptions exception

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """
    return Responder().fail(msg=http_exc.description, http_code=http_exc.code)
