import unittest
import os
from expungeservice.database import Database
from expungeservice.database import user


class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):

        password=""
        #password = os.environ['POSTGRES_PASSWORD']

        self.database = Database(host="localhost", port="5432", 
            name="record_expunge", username="postgres", 
            password=password)

    def test_database_connection(self):

        query = 'SELECT * FROM users;'
        self.database.cursor.execute(query, ())
        rows = self.database.cursor.fetchall()
        assert rows or rows == []

    def test_create_user(self):

        d