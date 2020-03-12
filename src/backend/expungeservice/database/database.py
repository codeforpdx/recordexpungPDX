"""Database module"""

import logging

import psycopg2
import psycopg2.extras
import os


class Database(object):
    """Database connection class.

Example usage:

import os
password = os.environ['POSTGRES_PASSWORD']
from expungeservice.database import database

# Get a connection.
db = database.Database(host='db', port='5432', name='record_expunge',
                       username='postgres', password=password)

# Run a query.
query = 'SELECT * FROM users;'
db.cursor.execute(query, ())

# Get the results.
rows = db.cursor.fetchall()

# Examine the results.
print(rows)
[row._asdict() for row in rows]
     """

    def __init__(self, host, port, name, username, password):
        """Opens a connection to the database."""
        self._host = host
        self._port = port
        self._name = name
        self._username = username
        self._conn = None
        self._cursor = None

        try:
            self._conn = psycopg2.connect(host=host, port=port, dbname=name, user=username, password=password)
            self._cursor = self._conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
            self._cursor.execute("""SET search_path TO {},public""".format(self._name))
        except psycopg2.OperationalError as e:
            logging.error(e)
            raise e

        psycopg2.extras.register_uuid()

    @property
    def host(self):
        """Returns database host."""
        return self._host

    @property
    def port(self):
        """Returns database port."""
        return self._port

    @property
    def name(self):
        """Returns database name."""
        return self._name

    @property
    def username(self):
        """Returns database username."""
        return self._username

    @property
    def connection(self):
        """Returns database connection."""
        return self._conn

    @property
    def cursor(self):
        """Returns connection cursor."""
        return self._cursor

    def close_connection(self):
        """Closes the connection."""
        if self._cursor is not None:
            self._cursor.close()

        if self._conn is not None:
            self._conn.close()

    def __str__(self):
        s = """Host: {}
Port: {}
Name: {}
Username: {}""".format(
            self.host, self.port, self.name, self.username
        )
        return s

def get_database():

    host = os.environ["PGHOST"]
    port = int(os.environ["PGPORT"])
    name = os.environ["PGDATABASE"]
    username = os.environ["PGUSERNAME"]
    password = os.environ["PGPASSWORD"]

    return Database(host=host, port=port, name=name, username=username, password=password)
