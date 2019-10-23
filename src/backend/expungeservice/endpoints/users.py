from flask.views import MethodView
from flask import request, abort, jsonify
from werkzeug.security import generate_password_hash

from flask import g
from expungeservice.database import user
from expungeservice.endpoints.auth import \
    user_auth_required, admin_auth_required
from expungeservice.request import check_data_fields
from psycopg2.errors import UniqueViolation
from expungeservice.request.error import error


class Users(MethodView):

    @user_auth_required
    def get(self, user_id):
        """
        Fetch a single user's data if a user_id is specified.
        Otherwise fetch the list of all users.
        Returned info contains user_id, name, group name,email,
        admin status, and date_created.
        """

        if user_id:

            user_db_data = user.read(g.database, user_id)

            if not user_db_data:
                error(404, "User id not recognized")

            if not g.logged_in_user_is_admin and g.logged_in_user_id != user_id:
                error(403, "Logged in user not admin and doesn't match requested user id.")

            response_data = {
                "user_id": user_db_data["user_id"],
                "email": user_db_data["email"],
                "name": user_db_data["name"],
                "group_name": user_db_data["group_name"],
                "admin": user_db_data["admin"],
                "timestamp": user_db_data["date_created"]}
            return jsonify(response_data), 201

        else:
            # No user_id given; this is a GET all users request.
            if not g.logged_in_user_is_admin:
                error(403, "Logged in user not admin ")

            user_db_data = user.fetchall(g.database)

            response_data = {"users": []}
            for user_entry in user_db_data:
                response_data["users"].append({
                    "user_id": user_entry["user_id"],
                    "email": user_entry["email"],
                    "name": user_entry["name"],
                    "group_name": user_entry["group_name"],
                    "admin": user_entry["admin"],
                    "timestamp": user_entry["date_created"]
                    })

            return jsonify(response_data), 201

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


    @user_auth_required
    def put(self, user_id):
        """
        Update the user entry with new values for one or more of the user data fields:
        email, name, group_name, password, or admin
        """
        user_db_data = user.read(g.database, user_id)
        if not user_db_data:
            error(404, "User id not recognized.")

        if not g.logged_in_user_is_admin and g.logged_in_user_id != user_id:
            error(403, "Logged in user not admin and doesn't match requested user id.")


        data = request.get_json()

        if data is None:
            error(400, "No json data in request body")

        if not any([key in data.keys() for key in ["email", "name", "group_name",
                                 "password", "admin"]]):

            error(400, "Json data must define one or more of: \
email, name, group_name, password, admin")

        if ("admin" in data.keys()) and (data["admin"] is True) and (not g.logged_in_user_is_admin):
            error(403, "Logged in user can not grant self admin privileges.")

        if "password" in data.keys():
            if len(data["password"]) < 8:
                error(422, "New password is less than 8 characters long.")
            data["hashed_password"] = generate_password_hash(data["password"])


        try:
            update_user_result = user.update(
                g.database,
                user_id,
                data)

        except UniqueViolation:
            error(422, "User with that email address already exists")

        if update_user_result is None:
            # Returns None if the user doesn't exist. We already checked this,
            # but if it still fails, throw 404
            error(404, "User id not recognized")

        response_data = {
            "user_id": update_user_result["user_id"],
            "email": update_user_result["email"],
            "admin": update_user_result["admin"],
            "name": update_user_result["name"],
            "group_name": update_user_result["group_name"],
            "timestamp": update_user_result["date_modified"]
        }
        return jsonify(response_data), 200


def register(app):
    user_view = Users.as_view('users')
    app.add_url_rule('/api/users', defaults={'user_id': None},
                     view_func=user_view,
                     methods=['GET'])

    app.add_url_rule('/api/users', view_func=user_view, methods=['POST'])
    app.add_url_rule('/api/users/<user_id>',
                     view_func=user_view,
                     methods=['GET', 'PUT'])
