import os
import datetime

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.urandom(32)
    JWT_EXPIRY_TIMER = datetime.timedelta(minutes=60)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_EXPIRY_TIMER = datetime.timedelta(minutes=60)

app_config = {
    'development': Development,
    'production': Production,
}
