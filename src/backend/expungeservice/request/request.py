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

    '''
    Acquiring db access information depending on the environment variables present.
    '''
    if os.environ.get('DATABASE_URL'):
        print("using database url: ", os.environ.get('DATABASE_URL'))
        infostr =  os.environ['DATABASE_URL'].split('postgres://')[1]
        creds, hostdat = infostr.split("@")
        #postgres://kkpsjvlphuqenz:dc7393549121483a1877d90de32b3c5b77b47af7f536567d31acb952128ce0bb@ec2-50-16-225-96.compute-1.amazonaws.com:5432/d98vao1s9j9t18

        print("got info from database_url")
        username = creds.split(":")[0]
        password = creds.split(":")[1]
        host = hostdat.split(":")[0]
        port = 5432
        name = hostdat.split("/")[1]
        print (host, port, name, username, password)

    else:
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
