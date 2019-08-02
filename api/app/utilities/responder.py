"""
Generic Data Response - contains a class used to keep data responses generic
"""

import json
import flask_sqlalchemy
from typing import Tuple
from flask import jsonify, Response


class Responder(object):
    """
    A base response object class to genericize responses
    """


    def __init__(self):
        self.success = False
        self.http_code = 501
        self.msg = "Not Implemented"
        self.results = []
        self.pagination = {}


    def succeed(self, msg:str=None, http_code:int=200) -> Tuple[Response, int]:
        """
        Respond with a success

        Args:
            msg (str, optional): Message to include in the response.
                                 Defaults to None.
            http_code (int, optional): HTTP status code.
                                       Defaults to 200.

        Returns:
            Tuple[Response, int]: [description]
        """
        self.success = True
        self.msg = msg
        self.http_code = http_code

        return self.response


    def fail(self, msg:str=None, http_code:int=500) -> Tuple[Response, int]:
        """
        Respond with a failure

        Args:
            msg (str, optional): Message to include in the response. 
                                 Defaults to None.
            http_code (int, optional): HTTP status code.
                                       Defaults to 500.

        Returns:
            Tuple[Response, int]: Flask Response & HTTP status code
        """
        self.success = False
        self.msg = msg
        self.http_code = http_code

        return self.response


    @property
    def as_dict(self) -> dict:
        """
        Return dictionary of self

        Returns:
            dict: Dictionary version of self
        """
        self_dict = self.__dict__
        # if we ever need to do things to the response just before it's
        # sent such as deleting certain properties we can do so here
        return self_dict


    @property
    def response(self) -> Tuple[Response, int]:
        """
        Create a flask jsonify response object with self dict as data,
        update the status code of the response, then return it.

        Returns:
            Tuple[Response, int]: Flask Response & HTTP status code
        """
        return (jsonify(self.as_dict), self.http_code)
