# /src/config.py

import os

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    JWT_SECRET_KEY = os.getenv('SECRET')

class Testing(object):
    """
    Development environment configuration
    """
    TESTING = True
    JWT_SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS=False

app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}


