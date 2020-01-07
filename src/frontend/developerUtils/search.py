from flask.views import MethodView
from flask import request, current_app
from flask_login import login_required

from expungeservice.models.helpers.generator import build_record
from expungeservice.request import check_data_fields
from expungeservice.request.error import error
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.crypto import DataCipher


class Search(MethodView):
    @login_required
    def post(self):
        request_data = request.get_json()

        if request_data is None:
            error(400, "No json data in request body")

        check_data_fields(request_data, ["first_name", "last_name", "middle_name", "birth_date"])

        cipher = DataCipher(key=current_app.config.get("SECRET_KEY"))

        decrypted_credentials = cipher.decrypt(request.cookies["oeci_token"])

        login_result = (
            decrypted_credentials["oeci_username"] == "username"
            and decrypted_credentials["oeci_password"] == "password"
        )
        if login_result is False:
            error(401, "Attempted login to OECI failed")

        record = build_record()
        response_data = {"data": {"record": record}}
        current_app.json_encoder = ExpungeModelEncoder

        return response_data  # Json-encoding happens automatically here


def register(app):
    app.add_url_rule("/api/search", view_func=Search.as_view("search"))
