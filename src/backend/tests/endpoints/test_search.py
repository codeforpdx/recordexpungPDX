import json

from expungeservice.endpoints import search
from tests.endpoints.endpoint_util import EndpointShared
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.serializer import ExpungeModelEncoder
import expungeservice
from expungeservice import stats


class TestSearch(EndpointShared):

    def setUp(self):
        EndpointShared.setUp(self)

        """ Save these actual function refs to reinstate after we're done mocking them."""
        self.crawler_login = search.Crawler.login
        self.search = search.Crawler.search
        self.save_result = search.save_result

        self.crawler = CrawlerFactory.setup()
        self.crawler.logged_in = True
        self.mock_record = {
            "john_doe": CrawlerFactory.create(self.crawler)
        }
        self.search_request_data = {
            "first_name": "John",
            "last_name": "Doe",
            "middle_name": "",
            "birth_date": "02/02/1990"}


    def tearDown(self):
        search.Crawler.login = self.crawler_login
        search.Crawler.search = self.search
        search.save_result = self.save_result


    def mock_login(self, return_value):
        return lambda s, username, password, close_session=False: return_value

    def mock_search(self, mocked_record_name):
        return lambda s, first_name, last_name, middle_name, birth_date: self.mock_record[mocked_record_name]

    def mock_save_result_fail(self, user_id, request_data, record):
        raise Exception("Exception to test failing save_result")

    def test_search(self):
        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])

        search.Crawler.login = self.mock_login(True)
        search.Crawler.search = self.mock_search("john_doe")

        """
        A separate test, below, verifies that the save-result step
        also works. Here, we mock the function to reduce the scope of the test.
        """
        search.save_result = lambda user_id, request_data, record : None

        """
        as a more unit-y unit test, we could make the encrypted cookie
        ""manually" in the test code ...
        But attaching a cookie client-side isn't really a thing. So, use the oeci endpoint.
        """

        self.client.post(
            "/api/oeci_login",
            json={"oeci_username": "correctusername",
                  "oeci_password": "correctpassword"})

        assert self.client.cookie_jar._cookies[
            "localhost.local"]["/"]["oeci_token"]


        response = self.client.post("/api/search",
            json=self.search_request_data)

        assert(response.status_code == 200)
        data = response.get_json()["data"]

        """
        Check that the resulting "record" field in the response matches what we gave to the
        mock search function.
        (use this json encode-decode approach because it turns a Record into a dict.)
        """
        assert data["record"] == json.loads(json.dumps(
            self.mock_record["john_doe"], cls = ExpungeModelEncoder))


    def test_search_fails_without_oeci_token(self):
        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])

        response = self.client.post("/api/search",
            json=self.search_request_data)

        assert(response.status_code == 401)


    def test_search_creates_save_results(self):
        """
        This is the same test as above except it includes the save-results step. Less unit-y,
        more of a vertical test.
        """

        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])

        search.Crawler.login = self.mock_login(True)
        search.Crawler.search = self.mock_search("john_doe")

        self.client.post(
            "/api/oeci_login",
            json={"oeci_username": "correctusername",
                  "oeci_password": "correctpassword"})

        assert self.client.cookie_jar._cookies[
            "localhost.local"]["/"]["oeci_token"]

        response = self.client.post("/api/search",
            json=self.search_request_data)

        assert(response.status_code == 200)
        data = response.get_json()["data"]

        """
        Check that the resulting "record" field in the response matches
        what we gave to the mock search function.

        (use this json encode-decode approach because it turns a Record into a dict.)
        """
        assert data["record"] == json.loads(json.dumps(
            self.mock_record["john_doe"], cls = ExpungeModelEncoder))


        self.check_search_result_saved(
            self.user_data["user1"]["user_id"], self.search_request_data,
            num_eligible_charges = 6, num_charges = 9)


    def test_search_with_failing_save_results(self):
        """
        The search endpoint should succeed even if something goes wrong with the save-result step.

        """

        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])
        search.Crawler.login = self.mock_login(True)
        search.Crawler.search = self.mock_search("john_doe")
        search.save_result = self. mock_save_result_fail

        self.client.post(
            "/api/oeci_login",
            json={"oeci_username": "correctusername",
                  "oeci_password": "correctpassword"})

        assert self.client.cookie_jar._cookies[
            "localhost.local"]["/"]["oeci_token"]


        response = self.client.post("/api/search",
            json=self.search_request_data)

        assert(response.status_code == 200)
        data = response.get_json()["data"]

        """
        Check that the resulting "record" field in the response matches what we gave to the
        mock search function.
        (use this json encode-decode approach because it turns a Record into a dict.)
        """
        assert data["record"] == json.loads(json.dumps(
            self.mock_record["john_doe"], cls = ExpungeModelEncoder))
