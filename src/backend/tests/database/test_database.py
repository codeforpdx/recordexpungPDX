import unittest
import pytest
import os
import psycopg2
from expungeservice.database import Database, user, get_database
from tests.endpoints.endpoint_util import EndpointShared

class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):

        self.database = get_database()

        self.db_cleanup()

        self.user_data = EndpointShared().user_data

    def tearDown(self):
        self.db_cleanup()

    def db_cleanup(self):
        cleanup_query = """DELETE FROM users where email like %(pattern)s;"""
        self.database.cursor.execute(cleanup_query, {"pattern": "%pytest%"})
        self.database.connection.commit()

    def test_database_connection(self):
        query = 'SELECT * FROM users;'
        self.database.cursor.execute(query, ())
        rows = self.database.cursor.fetchall()
        assert rows or rows == []

    def test_create_user_success(self):

        email = "pytest_create@example.com"
        name = "Ima Test"
        group_name = "Ima Test Group"
        hashed_password = "examplepasswordhash3"
        admin = True
        create_result = user.create(self.database, email, name,
                                    group_name, hashed_password, admin)

        assert create_result['email'] == email
        assert create_result['hashed_password'] == hashed_password
        assert create_result['name'] == name
        assert create_result['group_name'] == group_name
        assert create_result['admin'] == admin
        assert create_result['user_id']
        assert create_result['auth_id']
        assert create_result['date_created']
        assert create_result['date_modified']

        self.verify_user_data(email, name, group_name, hashed_password, admin)

    def test_create_user_duplicate_fail(self):

        email = "pytest_create_duplicate@example.com"
        name = "Ima Test",
        group_name = "Ima Test Group",
        hashed_password = 'examplepasswordhash'
        admin = True
        user.create(self.database, email, name, group_name,
                    hashed_password, admin)

        with pytest.raises(psycopg2.errors.UniqueViolation):
            user.create(self.database, email, name, group_name,
                        hashed_password, admin)

    def test_get_user(self):
        email = "pytest_get_user@example.com"
        name = "Ima Test"
        group_name = "Ima Test Group"
        hashed_password = 'examplepasswordhash2'
        admin = True

        self.create_example_user(email=email)

        user_result = user.read(
            self.database, user.identify_by_email(self.database, email))

        self.verify_user_data(
            user_result["email"],
            user_result["name"],
            user_result["group_name"],
            user_result["hashed_password"],
            user_result["admin"])

    def test_get_all_users(self):
        """
        test inserts two new users, then fetches from the table with the db
        get function and raw sql to compare the results. Checks the number of
        returned rows is the same, and that all of the columns match from
        each returned row.
        """

        email1 = "pytest_get_user@example.com"
        self.create_example_user(email1)

        email2 = "pytest_get_user_2@example.com"

        self.create_example_user(email2)

        users_get_endpoint_result = user.fetchall(self.database)

        verify_query = """
            SELECT * FROM USERS;"""
        self.database.cursor.execute(verify_query)

        verify_rows = [r._asdict() for r in self.database.cursor.fetchall()]

        assert len(verify_rows) == len(users_get_endpoint_result)

        for (email, name, group_name, hashed_password, admin) in [
                    (r['email'], r['name'], r['group_name'],
                     r['hashed_password'], r['admin'])
                    for r in users_get_endpoint_result]:

            self.verify_user_data(
                email, name, group_name, hashed_password, admin)

    def test_get_missing_user(self):

        email = "pytest_get_user_does_not_exist@example.com"

        user_result = user.read(self.database,
                                user.identify_by_email(self.database, email))

        assert user_result is None

    def test_update_password(self):

        self.create_example_user(self.user_data["user1"]["email"])
        user_id = user.identify_by_email(self.database, self.user_data["user1"]["email"])

        user.update(self.database, user_id, {"hashed_password": "new_hashed_password"})


        self.verify_user_data(
            self.user_data["user1"]["email"],
            self.user_data["user1"]["name"],
            self.user_data["user1"]["group_name"],
            "new_hashed_password",
            self.user_data["user1"]["admin"])

    def test_update_other_fields(self):

        self.create_example_user(self.user_data["user1"]["email"])
        user_id = user.identify_by_email(self.database, self.user_data["user1"]["email"])

        user.update(self.database, user_id,
                    {"email": "updated_pytest_@email.com",
                     "admin": True,
                     "name":"newname",
                     "group_name":"newgroupname"})


        self.verify_user_data(
            "updated_pytest_@email.com",
            "newname",
            "newgroupname",
            self.user_data["user1"]["hashed_password"],
            True)

    # Helper function
    def create_example_user(
        self,
        email=None,
        name=None,
        group_name=None,
        hashed_password=None,
        admin=None
        ):

        if email is None: email = self.user_data["user1"]["email"]
        if name is None: name = self.user_data["user1"]["name"]
        if group_name is None: group_name = self.user_data["user1"]["group_name"]
        if hashed_password is None: hashed_password = self.user_data["user1"]["hashed_password"]
        if admin is None: admin = self.user_data["user1"]["admin"]

        #print("user data: ", email, name)
        self.database.cursor.execute(
            """
            WITH USER_INSERT_RESULT AS
                (
                INSERT INTO USERS (user_id, email, name, group_name, admin)
                VALUES ( uuid_generate_v4(),
                    %(email)s,
                    %(name)s,
                    %(group_name)s,
                    %(adm)s)
                RETURNING user_id)
                INSERT INTO AUTH (auth_id, hashed_password, user_id)
                SELECT uuid_generate_v4(), %(pass)s, user_id
                FROM USER_INSERT_RESULT;
            """, {'email': email, 'pass': hashed_password, 'name': name,
                  'group_name': group_name, 'adm': admin})

        self.database.connection.commit()

    # Helper function
    def verify_user_data(self, email, name, group_name,
                         hashed_password, admin):
        # is passed the data obtained from the app function to be tested, e.g.
        # a database function or endpoint,
        # and checks that the fields match a second, raw SQL query.

        verify_query = """
            SELECT USERS.user_id::text, email, name, group_name, admin,
            hashed_password, auth_id::text, date_created, date_modified
            FROM USERS JOIN
            AUTH ON USERS.user_id = AUTH.user_id
            WHERE email = %(email)s;"""
        self.database.cursor.execute(verify_query, {'email': email})

        rows = self.database.cursor.fetchall()

        assert len(rows) == 1
        user_result = rows[0]._asdict()
        assert user_result['email'] == email
        assert user_result['name'] == name
        assert user_result['group_name'] == group_name
        assert user_result['hashed_password'] == hashed_password
        assert user_result['admin'] == admin
        assert user_result['user_id']
        assert user_result['auth_id']
        assert user_result['date_created']
        assert user_result['date_modified']
