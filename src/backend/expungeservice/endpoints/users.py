from flask.views import MethodView
from flask import request, abort, jsonify
from werkzeug.security import generate_password_hash

# TODO temp hack - replace with table from DB
users = {}

class Users(MethodView):
    def post(self):
        data = request.get_json()

        if data == None:
            abort(400)

        # TODO temp hack - replace with table from DB
        if data['username'] in users:
            return 'User already exists! Please login', 202

        users[data['username']] = generate_password_hash(data['password'])

        response_data = {
            'username': data['username'],
            'email address': data['email address']
        }

        return jsonify(response_data), 201

def register(app):
    app.add_url_rule('/api/v0.1/users', view_func=Users.as_view('users'))
