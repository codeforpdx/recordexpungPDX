from flask.views import MethodView
from flask import request, abort, jsonify
from werkzeug.security import generate_password_hash

from flask import g
from expungeservice.database import user
from expungeservice.endpoints.auth import admin_auth_required
from expungeservice.request import check_data_fields
from psycopg2.errors import UniqueViolation
from expungeservice.request.error import error


class User(MethodView):
    @admin_auth_required
    def post(self):
        """
        Create a new user with provided email, password, and admin flag.
        - If required fields are missing in the request, return 400
        - Password must be 8 or more characters long. Otherwise return 422
        - Email must not already be in use by an existing user.
          Otherwise return 422
        - If success, return 201 with the new user's email, admin flag,
          and creation timestamp.
        """

        data = request.get_json()

        if data is None:
            error(400, "No json data in request body")

        check_data_fields(data, ["email", "name", "group_name",
                                 "password", "admin"])

        if len(data["password"]) < 8:
            error(422, "New password is less than 8 characters long!")

        password_hash = generate_password_hash(data["password"])

        try:
            create_user_result = user.create(
                g.database,
                email=data["email"],
                name=data["name"],
                group_name=data["group_name"],
                password_hash=password_hash,
                admin=data["admin"])

        except UniqueViolation:
            error(422, "User with that email address already exists")

        response_data = {
            "user_id": create_user_result["user_id"],
            "email": create_user_result["email"],
            "admin": create_user_result["admin"],
            "name": create_user_result["name"],
            "group_name": create_user_result["group_name"],
            "timestamp": create_user_result["date_created"]

        }

        return jsonify(response_data), 201


def register(app):
    app.add_url_rule("/api/user", view_func=User.as_view("user"))
