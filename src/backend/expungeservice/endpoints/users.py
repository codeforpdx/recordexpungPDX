from flask.views import MethodView
from flask import request, abort, jsonify
from werkzeug.security import generate_password_hash

from flask import g
from expungeservice.database.user import create_user, get_user_by_email
from expungeservice.endpoints.auth import admin_auth_required
from expungeservice.request import check_data_fields
from psycopg2.errors import UniqueViolation


class Users(MethodView):
    @admin_auth_required
    def post(self):
        """
        Create a new user with provided email, password, and admin flag.
        - If required fields are missing in the request, return 400
        - Password must be 8 or more characters long. Otherwise return 422
        - Email must not already be in use by an existing user. Otherwise return 422
        If success, return 201 with the new user's email, admin flag, and creation timestamp.
        """

        data = request.get_json()

        if data == None:
            abort(400)

        check_data_fields(data, ['email', 'password', 'admin'])

        if len(data['password']) <8:
            return 'New password is less than 8 characters long!', 422

        password_hash = generate_password_hash(data['password'])

        try:
            create_user_result = create_user(g.database,
                                             email = data['email'],
                                             password_hash = password_hash,
                                             admin = data['admin'])
        except UniqueViolation:
            return 'User with that email address already exists!', 422

        response_data = {
            'email': create_user_result['email'],
            'admin': create_user_result['admin'],
            'timestamp': create_user_result['date_created'],
        }
        # user_id is not required by the frontend here so it is not included.
        # other endpoints may expose the user_id e.g. for other admin user-management operations.

        return jsonify(response_data), 201

def register(app):
    app.add_url_rule('/api/v0.1/users', view_func=Users.as_view('users'))
