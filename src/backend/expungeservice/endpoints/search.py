from flask.views import MethodView
from flask import request, abort, jsonify, current_app, g

from expungeservice.database import user
from expungeservice.request import check_data_fields
from expungeservice.request.error import error
from expungeservice.crawler.crawler import Crawler
from expungeservice.expunger.expunger import Expunger


class Search(MethodView):

    @user_auth_required
    def post(self):
        data = request.get_json()

        if data is None:
            error(400, "No json data in request body")

        check_data_fields(data, ["first_name", "last_name",
                                 "middle_name", "birthdate"])

        """
        Check the request has a cookie.
        """
        oeci_username, oeci_password = {}
        crawler = Crawler()
        login_result = crawler.login(oeci_username, oeci_password)

        first_name = data["first_name"]
        last_name = data["last_name"]
        middle_name = data["middle_name"]
        birthdate = data["birthdate"]

        record = crawler.search(first_name, last_name, middle_name, birth_date='')

        """
        record could be empty. check for that.
        """

        expunger = Expunger(record)

        response_data = {
            "record": record
        }

        return jsonify(response_data)


def register(app):
    app.add_url_rule("/api/search",
                     view_func=Search.as_view('search'))
