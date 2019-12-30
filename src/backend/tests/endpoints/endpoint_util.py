from flask.views import MethodView
from flask_login import login_required
from werkzeug.security import generate_password_hash
from flask import g
import hashlib

import expungeservice
from expungeservice.user import user_db_util
from expungeservice.user.user import admin_login_required

"""
protected-view template endpoints.
"""


class AdminProtectedView(MethodView):
    @admin_login_required
    def get(self):
        return "Admin-level Protected View"


class UserProtectedView(MethodView):
            @login_required
            def get(self):
                return "User-level Protected View"


class EndpointShared:

    user_data = {
        "user1":
        {
            "email": "pytest_user@auth_test.com",
            "name": "Endpoint Test",
            "group_name": "Endpoint Test Group",
            "admin": False,
            "password": "password",
            "hashed_password": generate_password_hash("password"),
        },
        "user2":
        {
            "email": "pytest_user2@auth_test.com",
            "name": "Endpoint Test2",
            "group_name": "Endpoint Test Group2",
            "admin": False,
            "password": "password2",
            "hashed_password": generate_password_hash("password2")
        },
        "admin": {
            "email": "pytest_admin@auth_test.com",
            "name": "Endpoint AdminTest",
            "group_name": "Endpoint AdminTest Group",
            "admin": True,
            "password": "admin",
            "hashed_password": generate_password_hash("admin")
        }
    }

    def create_test_user(self, user_key):

        create_result = user_db_util.create(
            g.database,
            self.user_data[user_key]["email"],
            self.user_data[user_key]["name"],
            self.user_data[user_key]["group_name"],
            self.user_data[user_key]["hashed_password"],
            self.user_data[user_key]["admin"]
        )
        self.user_data[user_key]["user_id"] = create_result["user_id"]

    def login(self, email, password):
        return self.client.post("/api/auth_token", json={
            "email": email,
            "password": password,
        })

    def setUp(self):

        self.app = expungeservice.create_app("development")
        self.client = self.app.test_client()

        self.app.add_url_rule(
            "/api/test/user_protected", view_func=UserProtectedView.as_view(
                "user_protected"))
        self.app.add_url_rule(
            "/api/test/admin_protected", view_func=AdminProtectedView.as_view(
                "admin_protected"))

        with self.app.app_context():
            expungeservice.request.before()
            self.db_cleanup()

            self.create_test_user("user1")
            self.create_test_user("user2")
            self.create_test_user("admin")
            g.database.connection.commit()

            expungeservice.request.teardown(None)

    def tearDown(self):
        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            expungeservice.request.teardown(None)

    def db_cleanup(self):

        search_result_cleanup_query = """
            DELETE FROM search_results
            where user_id in
                (SELECT user_id FROM users
                where email like %(pattern)s);"""
        g.database.cursor.execute(search_result_cleanup_query, {"pattern": "%pytest%"})

        cleanup_query = """DELETE FROM users where email like %(pattern)s;"""
        g.database.cursor.execute(cleanup_query, {"pattern": "%pytest%"})
        g.database.connection.commit()

    '''
    These functions are used for testing the search endpoint and stats-recording.
    '''

    def hash_search_params(self, user_id, request_data):
        search_param_string = (
            user_id +
            request_data["first_name"] +
            request_data["last_name"] +
            request_data["middle_name"] +
            request_data["birth_date"])

        hashed_search_params = hashlib.sha256(search_param_string.encode()).hexdigest()
        return hashed_search_params


    def check_search_result_saved(self, user_id, request_data,
            num_eligible_charges, num_charges):

        with self.app.app_context():
            expungeservice.request.before()

            hashed_search_params = self.hash_search_params(
                user_id, request_data)

            g.database.cursor.execute(
                """
                SELECT * FROM SEARCH_RESULTS
                WHERE hashed_search_params  = %(hashed_search_params)s
                ;
                """,{'hashed_search_params': hashed_search_params})

            result = g.database.cursor.fetchone()._asdict()

            assert result["num_eligible_charges"] == num_eligible_charges
            assert result["num_charges"] == num_charges
