"""
All custom error handlers for exceptions (HTTP and otherwise) needed 
must be here.

They will be registered when the application is started.
"""

import redis.exceptions as redis_exceptions
import sqlalchemy.exc as sqlalchemy_exceptions
from app.utilities.exceptions.exception_handlers import *

# Can add specific error handlers for specific http and other exceptions here
# by mapping it like <Exception>: <handler>
error_handlers = {
    redis_exceptions.ConnectionError: redis_conn_handler,
    sqlalchemy_exceptions.OperationalError: sqlalchemy_conn_handler,
     Exception: generic_exception_handler
}

# Add all HTTP exceptions handled by the generic_handler to the error handlers
# dict so they wil be registered
status_codes = [400, 404, 405, 409, 500, 501]
[error_handlers.update({err: generic_http_handler}) for err in status_codes]
