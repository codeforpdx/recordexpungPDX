import json

from expungeservice.endpoints import search
from tests.endpoints.endpoint_util import EndpointShared
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.serializer import ExpungeModelEncoder


class TestSearch(EndpointShared):

    def setUp(self):
        EndpointShared.setUp(self)

        """ Save these actual function refs to reinstate after we're done mocking them."""
        self.login = search.Crawler.login
        self.search = search.Crawler.search

        self.crawler = CrawlerFactory.setup()
        self.crawler.logged_in = True
        self.mock_record = {
            "john_doe": CrawlerFactory.create(self.crawler)
        }


    def tearDown(self):
        search.Crawler.login = self.login
        search.Crawler.search = self.search

    def mock_login(self, return_value):
        return lambda s, username, password, close_session=False: return_value

    def mock_search(self, mocked_record_name):
        return lambda s, first_name, last_name, middle_name, birth_date: self.mock_record[mocked_record_name]

    def test_search(self):

        search.Crawler.login = self.mock_login(True)
        search.Crawler.search = self.mock_search("john_doe")

        """
        as a more unit-y unit test, we could make the encrypted cookie
        ""manually" in the test code ...
        But attaching a cookie client-side isn't really a thing. So, use the oeci endpoint.
        """

        self.client.post(
            "/api/oeci_login", headers=self.user_data["user1"]["auth_header"],
            json={"oeci_username": "correctusername",
                  "oeci_password": "correctpassword"})

        assert self.client.cookie_jar._cookies[
            "localhost.local"]["/"]["oeci_token"]


        response = self.client.post("/api/search", headers=self.user_data["user1"]["auth_header"],
            json={"first_name": "John",
                  "last_name": "Doe",
                  "middle_name": "",
                  "birth_date": "02/02/1990"})

        assert(response.status_code == 200)
        data = response.get_json()["data"]

        """
        Check that the resulting "record" field in the response matches what we gave to the
        mock search function.
        (use this json encode-decode approach because it turns a Record into a dict.)
        """
        assert data["record"] == json.loads(json.dumps(
            self.mock_record["john_doe"], cls = ExpungeModelEncoder))
