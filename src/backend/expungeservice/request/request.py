from flask import g
import os
from expungeservice.database import Database


def before():

    host = os.environ['PGHOST']
    port = os.environ['PGPORT']
    name = os.environ['PGDATABASE']
    username = os.environ['PGUSER']
    password = os.environ['POSTGRES_PASSWORD']

    g.database = Database(
        host=host,
        port=port,
        name=name,
        username=username,
        password=password)

def teardown(exception):
    g.database.close_connection()
