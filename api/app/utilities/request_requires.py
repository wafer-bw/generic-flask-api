"""
Decorators used to ensure requirements of requests are met
"""

import json
from flask import request
from functools import wraps
from app.utilities.helpers import load_json
from werkzeug.exceptions import BadRequest


def headers(headers:dict):
    """
    Decorator which raises a BadRequest() exception if the required
    header key value pairs are not present in the request headers.

    Args:
        headers (dict): Required headers

    Raises:
        BadRequest: If the request does not contain the required headers
    """
    def decorator(original_function):
        @wraps(original_function)
        def wrapper(*args, **kwargs):
            h = request.headers
            mh = {k: v for k, v in headers.items() if k not in h or h[k] != v}
            if mh:
                raise BadRequest(f"Bad Request - Missing Headers: {mh}")
            return original_function(*args, **kwargs)
        return wrapper
    return decorator
