from flask import g, abort
import os
from expungeservice.database import Database
from expungeservice.request.error import error

def before():
    host = os.environ['PGHOST']
    port = os.environ['PGPORT']
    name = os.environ['PGDATABASE']
    username = os.environ['POSTGRES_USERNAME']
    password = os.environ['POSTGRES_PASSWORD']

    g.database = Database(
        host=host,
        port=port,
        name=name,
        username=username,
        password=password)

def teardown(exception):
    g.database.close_connection()

def check_data_fields(request_json, required_fields):

    if not all([field in request_json.keys() for field in required_fields]):
        error(400, "missing one or more required fields: " + str(required_fields))
