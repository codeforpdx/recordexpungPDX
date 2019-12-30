import unittest
import expungeservice
from flask import g

from expungeservice.database import get_database


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = expungeservice.app.create_app('development')
        self.test_client = self.app.test_client()


    def test_get_database_connection(self):

        with self.app.app_context():

            g.database = get_database()

            assert g.database

            query = 'SELECT * FROM users;'
            g.database.cursor.execute(query, ())
            rows = g.database.cursor.fetchall()
            assert rows or rows == []

            g.database.close_connection()
            assert g.database.cursor.closed
