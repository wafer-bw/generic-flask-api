"""
Flask App Config Objects

http://flask.pocoo.org/docs/1.0/config/

Note: Only uppercase variables will be imported into flask app config.
"""

import os

dev_cli_choices = ("Testing", "Dev")


class Config(object):
    DEBUG = False
    TESTING = False

    DB_DIALECT = "mysql+pymysql"
    DB_HOST = os.getenv("DB_HOST", "0.0.0.0")
    DB_PORT = os.getenv("DB_PORT", 3306)
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASS = os.getenv("MYSQL_ROOT_PASSWORD", "defaultpassword")
    DB_NAME = os.getenv("DB_NAME", "exampledb")

    uri = f"{DB_DIALECT}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = os.getenv("CACHE_REDIS_HOST", "0.0.0.0")
    CACHE_REDIS_PORT = os.getenv("CACHE_REDIS_PORT", 6379)
    CACHE_REDIS_PASSWORD = os.getenv("CACHE_REDIS_PASSWORD", None)
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 30))

    BCRYPT_LOG_ROUNDS = int(os.getenv("BCRYPT_LOG_ROUNDS", 6))


class TestingConfig(Config):
    TESTING = True


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    pass
