import jwt
import functools
import datetime

from flask.views import MethodView
from flask import request, abort, jsonify, current_app, g
from werkzeug.security import check_password_hash

from expungeservice.database import user
from expungeservice.request import check_data_fields
from expungeservice.request.error import error


def get_auth_token(app, user_id):
    dt = datetime.datetime.utcnow()
    payload = {
        'iss': 'expungeservice',
        'iat': dt,
        'exp': dt + app.config.get('JWT_EXPIRY_TIMER'),
        'sub': user_id,
    }
    return jwt.encode(
        payload,
        app.config.get('JWT_SECRET_KEY'),
        algorithm='HS256'
    ).decode('utf-8')


def user_auth_required(f):
    """Verifies the auth token identifying the logged in user.
    If the auth token is missing or invalid, return 401 UNAUTHORIZED."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return authorized(f, False, *args, **kwargs)
    return wrapper


def admin_auth_required(f):
    """Verifies the auth token identifying the logged in user is admin.
    If the auth token is missing or invalid, return 401 UNAUTHORIZED.
    If the user is not admin, return 403 FORBIDDEN."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return authorized(f, True, *args, **kwargs)
    return wrapper


def authorized(f, admin_required, *args, **kwargs):
    try:
        auth_hdr = request.headers.get('Authorization')
        if auth_hdr is None:
            error(401, 'Missing Authorization header')

        auth_hdr_split = auth_hdr.split("Bearer")
        if not len(auth_hdr_split) == 2:
            error(401, 'Malformed auth token string, \
                should be: "Bearer [auth_string]"')

        payload = jwt.decode(
            auth_hdr_split[1].strip(),
            current_app.config.get('JWT_SECRET_KEY'),
            algorithms=["HS256"]
        )

        user_data = user.read(g.database, payload['sub'])
        if user_data == []:
            error(401, 'Invalid auth token claim')

        if admin_required and not user_data['admin']:
            error(403, 'Logged in user not admin')

        g.logged_in_user_id = user_data['user_id']
        g.logged_in_user_is_admin = user_data['admin']

        return f(*args, **kwargs)

    except (
            jwt.exceptions.InvalidTokenError,
            jwt.exceptions.InvalidSignatureError,
    ):
        error(401, 'Invalid auth token, signature verification failed')
    except jwt.exceptions.ExpiredSignatureError:
        error(401, 'Auth token expired')


class AuthToken(MethodView):
    def post(self):
        data = request.get_json()

        if data is None:
            error(400, "No json data in request body")

        check_data_fields(data, ['email', 'password'])

        user_db_result = user.read(
            g.database,
            user.identify_by_email(g.database, data['email']))

        if (not user_db_result or
                not check_password_hash(user_db_result['hashed_password'],
                                        data['password'])):
            error(401, 'Invalid username or password')

        response_data = {
            'auth_token': get_auth_token(current_app,
                                         user_db_result['user_id']),
            'user_id': user_db_result['user_id']
        }
        return jsonify(response_data)


def register(app):
    app.add_url_rule('/api/auth_token',
                     view_func=AuthToken.as_view('auth_token'))
