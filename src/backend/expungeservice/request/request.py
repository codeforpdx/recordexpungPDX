from flask import g, abort
from expungeservice.database import get_database
from expungeservice.request.error import error

def before():


    g.database = get_database()

def teardown(exception):
    g.database.close_connection()

def check_data_fields(request_json, required_fields):

    if not all([field in request_json.keys() for field in required_fields]):
        error(400, "missing one or more required fields: " + str(required_fields))
