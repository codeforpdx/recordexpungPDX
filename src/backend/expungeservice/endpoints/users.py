from flask.views import MethodView
from flask import request, abort, jsonify
from werkzeug.security import generate_password_hash

from flask import g
from expungeservice.database import user
from expungeservice.endpoints.auth import admin_auth_required
from expungeservice.request import check_data_fields
from psycopg2.errors import UniqueViolation
from expungeservice.request.error import error


class Users(MethodView):

    @admin_auth_required
    def get(self):
        """
        Fetch the list of users, including their email, admin clear
        """

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


def register(app):
    app.add_url_rule("/api/users", view_func=Users.as_view("users"))
