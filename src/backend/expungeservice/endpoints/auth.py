from flask.views import MethodView
from flask import request, make_response, g
from flask_login import login_required, logout_user
from flask_login.login_manager import LoginManager
from werkzeug.security import check_password_hash
from dacite import from_dict
import time

from expungeservice.request import check_data_fields
from expungeservice.request import error
from expungeservice.user import user_db_util
from expungeservice.user.user import User


class AuthToken(MethodView):
    def post(self):
        data = request.get_json()

        if data is None:
            error(400, "No json data in request body")

        check_data_fields(data, ["email", "password"])

        user_db_result = user_db_util.read(g.database, user_db_util.identify_by_email(g.database, data["email"]))

        if not user_db_result or not check_password_hash(user_db_result["hashed_password"], data["password"]):
            error(401, "Invalid username or password")

        user = from_dict(data_class=User, data=user_db_result)
        User.login_user(user)

        response = make_response()
        if user.admin:
            response.set_cookie(
                "is_admin",
                expires=time.time() + 365 * 24 * 60 * 60,  # type: ignore # 1 year lifetime matches flask login cookie
            )
        return response, 200


class Logout(MethodView):
    @login_required
    def post(self):
        logout_user()
        return "Success"


def __user_loader(user_id):
    user_db_result = user_db_util.read(g.database, user_id)
    return from_dict(data_class=User, data=user_db_result)


def register(app):
    app.add_url_rule("/api/auth_token", view_func=AuthToken.as_view("auth_token"))
    app.add_url_rule("/api/logout", view_func=Logout.as_view("logout"))

    app.secret_key = app.config.get("SECRET_KEY")
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(__user_loader)
