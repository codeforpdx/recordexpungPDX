import os
import datetime

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.urandom(24)
    JWT_EXPIRY_TIMER = datetime.timedelta(seconds=60)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = 'insecurekeyfordev'

    # Celery.
    #todo Secure this before launch
    CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 5

    # SQLAlchemy.
    #TODO change this before launch
    db_uri = 'postgresql://recordexpung:devpassword@postgres:5432/recordexpung'
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    SECRET_KEY = 'insecurekeyfordev'

    # Celery.
    #todo Secure this before launch
    CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 5

    # SQLAlchemy.
    #TODO change this before launch
    db_uri = 'postgresql://recordexpung:devpassword@postgres:5432/recordexpung'
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False



    JWT_EXPIRY_TIMER = datetime.timedelta(minutes=10)


app_config = {
    'development': Development,
    'production': Production,
}
