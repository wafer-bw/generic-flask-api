"""
A collection of helper utilities
"""

import json
import flask_sqlalchemy
from flask import request
from flask_sqlalchemy import Pagination
from werkzeug.exceptions import BadRequest


def load_json(data:object) -> dict:
    """
    Load JSON from data object which is typically bytes or str.
    is encountered than a bad request is raised.
    
    Args:
        data (object): String or Bytes object of data
    
    Raises:
        BadRequest: If JSONDecodeError is raised then we got bad data.
    
    Returns:
        dict: JSON loaded data
    """
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        raise BadRequest("Bad Request - Missing/invalid POST data/headers.")


def pagination_dict(pgn: Pagination, mask:list=[]) -> dict:
    """
    For some reason flask_sqlalchemy.Pagination does not have a 
    serialization method so this is a patch to get all the properties we
    want from a Pagination object.
    https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination

    Args:
        pgn (flask_sqlalchemy.Pagination): Flask SQLAlchemy Pagination Object
        mask (list, optional): Defaults to [] - Mask the keys of 
                               properties to exclude from output dict
                               available keys are:
                                    has_next (bool): has next page
                                    next_num (int): next page
                                    has_prev (bool): has previous page
                                    prev_num (int): previous page
                                    page (int): current page
                                    pages (int): total page count
                                    per_page (int): results per page
                                    total (int): total result count

    Returns:
        dict: Pagination information dictionary
    """
    p = {}
    src = {"has_next": pgn.has_next, "next_num": pgn.next_num,
           "has_prev": pgn.has_prev, "prev_num": pgn.prev_num,
           "page": pgn.page, "pages": pgn.pages, "per_page": pgn.per_page,
           "total": pgn.total,}

    [p.update({k:v}) for k, v in src.items() if k not in mask]
    return p


def is_jsonable(obj: object) -> bool:
    """
    Check if an object can be converted to JSON

    Args:
        obj (object): Object to check

    Returns:
        bool: True if object can be converted to JSON, False otherwise
    """
    try:
        json.dumps(obj)
        return True
    except Exception:
        return False
