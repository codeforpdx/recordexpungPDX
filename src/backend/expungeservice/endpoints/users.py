from flask.views import MethodView
from flask import request, abort, jsonify
from werkzeug.security import generate_password_hash

from flask import g
from expungeservice.database.user import create_user, get_user_by_email
from expungeservice.endpoints.auth import auth_required
from psycopg2.errors import UniqueViolation


class Users(MethodView):
    @auth_required
    def post(self):
        data = request.get_json()

        if data == None:
            abort(400)

        """
        - the @auth_required decorator identifies the logged in user. If no auth, return 401 UNAUTHORIZED.
        - Verify the logged in user is admin. if not, return 403 FORBIDDEN.
        - Verify the password meets the 8-character length requirement. If not, return 422
        - Attempt to insert the user into the database. If failure due to duplicate entry, return 422
        - If success, return the new user's email, admin flag, and creation timestamp.
        """

        authorized_user_db_result = get_user_by_email(g.database, g.auth_hdr_payload['sub'])
        if not authorized_user_db_result['admin']:
            return 'Logged in user not admin', 403

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

        return jsonify(response_data), 201

def register(app):
    app.add_url_rule('/api/v0.1/users', view_func=Users.as_view('users'))
