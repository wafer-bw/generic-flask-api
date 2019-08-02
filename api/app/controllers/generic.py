"""
Generic controller for interacting with models in the database.
"""

import json
from typing import Tuple
from sqlalchemy.exc import *
from werkzeug.exceptions import *
from flask import jsonify, request, Blueprint, Response

from app.models import models
from app.utilities import request_requires
from app.utilities.extensions.cache import cache
from app.utilities.helpers import load_json, pagination_dict
from app.utilities.responder import Responder

generic_bp = Blueprint("generic", __name__)


@generic_bp.route("<string:model>", methods=["POST"])
@request_requires.headers({"Content-Type": "application/json"})
def create(model:str) -> Tuple[Response, int]:
    """
    Create model item, adding it to the database.

    Args:
        model (str): Name of model of the item to create

    Raises:
        BadRequest: Improper/missing POST data
        BadRequest: Model does not exist
        Conflict: Item already exists

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """
    try:
        item = models[model](**load_json(request.data))
        item.save()

        return Responder().succeed(msg=f"Created {item}")

    except TypeError:
        raise BadRequest(f"Improper/missing POST data")

    except KeyError:
        raise BadRequest(f"{model} does not exist")

    except IntegrityError:
        raise Conflict(f"{item} already exists")


@generic_bp.route("<string:model>/<int:_id>", methods=["GET"])
@cache.cached()
def read_by_id(model:str, _id:int) -> Tuple[Response, int]:
    """
    Get an item in the model DB by ID from URL path and cache the result

    Args:
        model (str): Name of model of the item to request by ID
        _id (int): ID of the item being requested

    Raises:
        NotFound: Item does not exist
        BadRequest: Model does not exist

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """
    try:
        item = models[model].query.filter_by(id=_id).first()

        if not item:
            raise NotFound(f"{model} {_id} does not exist")

        responder = Responder()
        responder.results.append(item.as_dict)
        return responder.succeed()

    except KeyError:
        raise BadRequest(f"{model} does not exist")


@generic_bp.route("<string:model>", methods=["GET"])
def read_all(model:str) -> Tuple[Response, int]:
    """
    Get all items in the model (paginated)

    Args:
        model (str): Name of model of the items

    Query Params:
        page (int): Requested page number
        per_page (int): Requested number of items to return per page

    Raises:
        BadRequest: Model does not exist

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """

    @cache.memoize()
    def get_all_paginated_results(**kwargs) -> Tuple[Response, int]:
        """
        You may notice the kwargs object isn't used in this nested
        function, it is only used by the cache.memoize decorator, so
        that the results for pagination query params like 
        "?per_page=2&page=4" aren't cached the same as others like:
        "?per_page=3&page=2".

        Note: It may be faster/better to un-nest this later

        Returns:
            Tuple[Response, int]: Flask Response & HTTP status code
        """

        results = models[model].query.paginate(error_out=False)

        if not results:
            return Responder().succeed(msg=f"No {model} results found")

        responder = Responder()
        responder.results += [item.as_dict for item in results.items]
        responder.pagination = pagination_dict(results)

        return responder.succeed()

    try:
        return get_all_paginated_results(**dict(request.args))
    except KeyError:
        raise BadRequest(f"{model} does not exist")


@generic_bp.route("<string:model>/<int:_id>", methods=["PUT"])
@request_requires.headers({"Content-Type": "application/json"})
def update(model:str, _id:int) -> Tuple[Response, int]:
    """
    Update model item's record in the database by ID

    Args:
        model (str): Name of model of the item to update by ID
        _id (int): ID of the item being updated

    Raises:
        NotFound: Item does not exist
        BadRequest: Improper/missing POST data
        BadRequest: Model does not exist
        Conflict: Item in updated state already exists (idempotency)

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """
    try:
        item = models[model].query.filter_by(id=_id).first()
        item.update(id=_id, **load_json(request.data))

        return Responder().succeed(msg=f"Updated {model} {_id}")

    except AttributeError:
        raise NotFound(f"{model} {_id} does not exist")

    except TypeError:
        raise BadRequest(f"Improper/missing POST data")

    except KeyError:
        raise BadRequest(f"{model} does not exist")

    except IntegrityError:
        raise Conflict(f"Item already exists")


@generic_bp.route("<string:model>/<int:_id>", methods=["DELETE"])
def delete(model:str, _id:int) -> Tuple[Response, int]:
    """
    Delete model item's record from the database by ID

    Args:
        model (str): Name of model of the item to delete by ID
        _id (int): ID of the item being deleted

    Raises:
        NotFound: Item does not exist
        BadRequest: Model does not exist

    Returns:
        Tuple[Response, int]: Flask Response & HTTP status code
    """
    try:
        item = models[model].query.filter_by(id=_id).first()

        if not item:
            raise NotFound(f"{model} {_id} does not exist")

        item.delete()

        return Responder().succeed(msg=f"Deleted {model} {_id}!")

    except KeyError:
        raise BadRequest(f"{model} does not exist")
