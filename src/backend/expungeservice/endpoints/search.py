from flask.views import MethodView
from flask import request, abort, current_app, g
import json

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
                                 "middle_name", "birth_date"])

        """
        Check the request has a cookie,
        Extract / decrypt the oeci login username and password

        If these fail, return 400 error
        """

        oeci_username, oeci_password = {}


        crawler = Crawler()
        login_result = crawler.login(oeci_username, oeci_password)

        first_name = data["first_name"]
        last_name = data["last_name"]
        middle_name = data["middle_name"]
        birth_date = data["birth_date"]

        record = crawler.search(first_name, last_name, middle_name, birth_date)

        """
        If the crawler returns nothing, don't expunge.
        """
        if record:
            expunger = Expunger(record)
            expunger.run()

        response_data = {
            "record": record
        }

        return json.dumps(response_data, cls=ExpungeModelEncoder)


def register(app):
    app.add_url_rule("/api/search",
                     view_func=Search.as_view('search'))
