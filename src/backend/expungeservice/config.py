import os
import datetime


class Development(object):
    """
    Development environment configuration
    """

    DEBUG = True
    TESTING = False
    SECRET_KEY = "1234567890987654321234567890987654321234567890987654321234567890987654321234567890987654321234567"
    JWT_EXPIRY_TIMER = datetime.timedelta(minutes=60)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SESSION_COOKIE_SECURE = False


class Production(object):
    """
    Production environment configurations
    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_EXPIRY_TIMER = datetime.timedelta(minutes=60)
    SESSION_COOKIE_SECURE = True


app_config = {
    "development": Development,
    "production": Production,
}
