import jwt
import functools
import datetime
import re

from flask.views import MethodView
from flask import request, abort, jsonify, current_app, g
from werkzeug.security import check_password_hash

from expungeservice.database.user import get_user_by_email

def get_auth_token(app, email):
    dt = datetime.datetime.utcnow()
    payload = {
        'iss': 'expungeservice',
        'iat': dt,
        'exp': dt + app.config.get('JWT_EXPIRY_TIMER'),
        'sub': email,
    }
    return jwt.encode(
        payload,
        app.config.get('JWT_SECRET_KEY'),
        algorithm='HS256'
    ).decode('utf-8')

def auth_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            auth_hdr = request.headers.get('Authorization')
            if auth_hdr == None:
                return 'Missing Authorization header!', 401

            match = re.match('Bearer +(.+)', auth_hdr)

            if match == None:
                abort(400)

            payload = jwt.decode(
                match.group(1),
                current_app.config.get('JWT_SECRET_KEY')
            )

            g.auth_hdr_payload = payload

            user_db_result = get_user_by_email(g.database, payload['sub'])
            if user_db_result == []:
                return 'Invalid auth token claim!', 401

            return f(*args, **kwargs)
        except (
                jwt.exceptions.InvalidTokenError,
                jwt.exceptions.InvalidSignatureError,
        ):
            return 'Invalid auth token!', 401
        except jwt.exceptions.ExpiredSignatureError:
            return 'auth token expired!', 401
    return wrapper

class AuthToken(MethodView):
    def get(self):
        data = request.get_json()

        if data == None:
            abort(400)
        user_db_result = get_user_by_email(g.database, data['email'])

        if (not user_db_result or
                not check_password_hash(user_db_result['hashed_password'], data['password'])):
            return 'Unauthorized', 401

        response_data = {
            'auth_token': get_auth_token(current_app, data['email'])
        }
        return jsonify(response_data)

def register(app):
    app.add_url_rule('/api/v0.1/auth_token', view_func=AuthToken.as_view('auth_token'))
