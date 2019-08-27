import unittest
import pytest
import os
import psycopg2
from expungeservice.database import Database, user, get_database


class TestDatabaseOperations(unittest.TestCase):


    def setUp(self):

        self.database = get_database()

        self.db_cleanup()

    def tearDown(self):
        self.db_cleanup()

    def db_cleanup(self):
        cleanup_query = """DELETE FROM users where email like %(pattern)s;"""
        self.database.cursor.execute(cleanup_query, {"pattern":"%pytest%"})
        self.database.connection.commit()

    def test_database_connection(self):
        query = 'SELECT * FROM users;'
        self.database.cursor.execute(query, ())
        rows = self.database.cursor.fetchall()
        assert rows or rows == []

    def test_create_user_success(self):

        email = "pytest_create@example.com"
        hashed_password = "examplepasswordhash3"
        admin = True
        create_result = user.create_user(self.database, email, hashed_password, admin)

        assert create_result['email'] == email
        assert create_result['hashed_password'] == hashed_password
        assert create_result['admin'] == admin
        assert create_result['user_id']
        assert create_result['auth_id']
        assert create_result['date_created']
        assert create_result['date_modified']

        self.verify_user_data(email, hashed_password, admin)

    def test_create_user_duplicate_fail(self):

        email = "pytest_create_duplicate@example.com"
        hashed_password = 'examplepasswordhash'
        admin = True
        user.create_user(self.database, email, hashed_password, admin)

        with pytest.raises(psycopg2.errors.UniqueViolation):
            user.create_user(self.database, email, hashed_password, admin)

    def test_get_user(self):
        email = "pytest_get_user@example.com"
        hashed_password = 'examplepasswordhash2'
        admin = True

        self.create_example_user(email, hashed_password, admin)

        user_result = user.get_user_by_email(self.database, email)

        self.verify_user_data(email, hashed_password, admin)

    def test_get_missing_user(self):

        email = "pytest_get_user_does_not_exist@example.com"

        user_result = user.get_user_by_email(self.database, email)

        assert user_result == None

    #Helper function
    def create_example_user(self, email, hashed_password, admin):

        self.database.cursor.execute(
        """
        WITH USER_INSERT_RESULT AS
            (
            INSERT INTO USERS (user_id, email, admin)
            VALUES ( uuid_generate_v4(), %(email)s, %(adm)s)
            RETURNING user_id)
            INSERT INTO AUTH (auth_id, hashed_password, user_id)
            SELECT uuid_generate_v4(), %(pass)s, user_id FROM USER_INSERT_RESULT;
        """, {'email':email, 'pass':hashed_password, 'adm': admin})

        self.database.connection.commit()

    #Helper function
    def verify_user_data(self, email, hashed_password, admin):

        verify_query = """
            SELECT USERS.user_id::text, email, admin, hashed_password, auth_id::text, date_created, date_modified
            FROM USERS JOIN
            AUTH ON USERS.user_id = AUTH.user_id
            WHERE email = %(email)s;"""
        self.database.cursor.execute(verify_query, {'email':email})

        rows = self.database.cursor.fetchall()

        assert len(rows) == 1
        user_result = rows[0]._asdict()
        assert user_result['email'] == email
        assert user_result['hashed_password'] == hashed_password
        assert user_result['admin'] == admin
        assert user_result['user_id']
        assert user_result['auth_id']
        assert user_result['date_created']
        assert user_result['date_modified']
