from flask import g, request


import expungeservice
from expungeservice.database.db_util import rollback_errors
from expungeservice import stats
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.database import get_database
from tests.endpoints.endpoint_util import EndpointShared
from flask.views import MethodView


class TestStatsView(MethodView):
    """
    To get the direct call to stats.save_result() to work,
    this endpoint wrapper is needed so that the flask.current_user
    object gets populated with user_id
    """

    def post(self):

        request_data = request.get_json()
        record = CrawlerFactory.create(CrawlerFactory.setup())
        stats.save_result(request_data, record)

        return "TestStatsViewResponse"


class TestStats(EndpointShared):


    def test_save_result(self):

        self.app.add_url_rule(
            "/api/test/save_result", view_func=TestStatsView.as_view(
                "save_result"))

        user_id = self.user_data["user1"]["user_id"]

        request_data = {
            "first_name":"John",
            "last_name":"Doe",
            "middle_name":"Test",
            "birth_date":"01/01/1980",
        }

        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])

        response = self.client.post('/api/test/save_result', json = request_data)

        self.check_search_result_saved(
                    self.user_data["user1"]["user_id"], request_data,
                    num_eligible_charges=6, num_charges=9)
