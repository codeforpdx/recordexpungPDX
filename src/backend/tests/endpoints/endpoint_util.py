import unittest
from werkzeug.security import generate_password_hash

import expungeservice
from expungeservice.endpoints.auth import *


"""
protected-view template endpoints.
"""


class AdminProtectedView(MethodView):
    @admin_auth_required
    def get(self):
        return "Admin-level Protected View"


class UserProtectedView(MethodView):
            @user_auth_required
            def get(self):
                return "User-level Protected View"


class EndpointShared(unittest.TestCase):

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

        create_result = user.create(
            g.database,
            self.user_data[user_key]["email"],
            self.user_data[user_key]["name"],
            self.user_data[user_key]["group_name"],
            self.user_data[user_key]["hashed_password"],
            self.user_data[user_key]["admin"]
        )
        self.user_data[user_key]["user_id"] = create_result["user_id"]

        generate_auth_response = self.generate_auth_token(
            self.user_data[user_key]["email"],
            self.user_data[user_key]["password"]
        )

        self.user_data[user_key]["auth_header"] = {"Authorization": "Bearer {}".format(
                generate_auth_response.get_json()["auth_token"])}

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
            expungeservice.request.teardown(None)

        with self.app.app_context():
            expungeservice.request.before()
            res = self.create_test_user("user1")
            expungeservice.request.teardown(None)

        with self.app.app_context():
            expungeservice.request.before()
            self.create_test_user("user2")
            expungeservice.request.teardown(None)

        with self.app.app_context():
            expungeservice.request.before()
            self.create_test_user("admin")
            expungeservice.request.teardown(None)

    def tearDown(self):
        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            expungeservice.request.teardown(None)

    def db_cleanup(self):

        cleanup_query = """DELETE FROM users where email like %(pattern)s;"""
        g.database.cursor.execute(cleanup_query, {"pattern": "%pytest%"})
        g.database.connection.commit()

    def generate_auth_token(self, email, password):
        return self.client.post("/api/auth_token", json={
            "email": email,
            "password": password,
        })
