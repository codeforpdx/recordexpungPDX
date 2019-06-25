import jwt
import functools
import datetime

from flask.views import MethodView
from flask import request, abort, jsonify, current_app, g
from werkzeug.security import check_password_hash

from expungeservice.database.user import get_user_by_email, get_user_by_id
from expungeservice.request import check_data_fields


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
        if auth_hdr == None:
            return 'Missing Authorization header!', 401

        auth_hdr_split =  auth_hdr.split("Bearer")
        if not len(auth_hdr_split) == 2:
            return 'Invalid auth token!', 401

        payload = jwt.decode(
            auth_hdr_split[1].strip(),
            current_app.config.get('JWT_SECRET_KEY')
        )

        user_data = get_user_by_id(g.database, payload['sub'])
        if user_data == []:
            return 'Invalid auth token claim!', 401

        if admin_required and not user_data['admin']:
            return 'Logged in user not admin', 403

        #no endpoint code uses the logged in user_id so this is commented for now. This may change.
        #g.logged_in_user_id = user_data['user_id']

        return f(*args, **kwargs)

    except (
            jwt.exceptions.InvalidTokenError,
            jwt.exceptions.InvalidSignatureError,
    ):
        return 'Invalid auth token!', 401
    except jwt.exceptions.ExpiredSignatureError:
        return 'auth token expired!', 401

class AuthToken(MethodView):
    def get(self):
        data = request.get_json()

        if data == None:
            abort(400)

        check_data_fields(data, ['email', 'password'])

        user_db_result = get_user_by_email(g.database, data['email'])

        if (not user_db_result or
                not check_password_hash(user_db_result['hashed_password'], data['password'])):
            return 'Unauthorized', 401

        response_data = {
            'auth_token': get_auth_token(current_app, user_db_result['user_id'])
        }
        return jsonify(response_data)

def register(app):
    app.add_url_rule('/api/v0.1/auth_token', view_func=AuthToken.as_view('auth_token'))
