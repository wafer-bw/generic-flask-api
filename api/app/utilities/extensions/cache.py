"""
Flask Cache Extension
https://flask-caching.readthedocs.io/en/latest/

This must be registered to the app within app/factory.py

Note: If caching view/controller then place after route decorator
on controller/view or else it will cache wrong.
"""

from flask_caching import Cache

cache = Cache()
