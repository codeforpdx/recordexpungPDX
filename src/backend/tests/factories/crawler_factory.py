import requests_mock

from expungeservice.crawler.request import URL
from expungeservice.models.record import Record
from expungeservice.record_creator import RecordCreator
from tests.fixtures.post_login_page import PostLoginPage
from tests.fixtures.search_page_response import SearchPageResponse
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe


class CrawlerFactory:
    @staticmethod
    def create(
        record=JohnDoe.RECORD_WITH_CLOSED_CASES,
        cases={"X0001": CaseDetails.case_x(), "X0002": CaseDetails.case_x(), "X0003": CaseDetails.case_x()},
    ) -> Record:
        base_url = "https://publicaccess.courts.oregon.gov/PublicAccessLogin/"
        with requests_mock.Mocker() as m:
            m.post(URL.login_url(), text=PostLoginPage.POST_LOGIN_PAGE)

            m.post(
                "{}{}".format(base_url, "Search.aspx?ID=100"), [{"text": SearchPageResponse.RESPONSE}, {"text": record}]
            )

            for key, value in cases.items():
                m.get("{}{}{}".format(base_url, "CaseDetail.aspx?CaseID=", key), text=value)

            aliases = [{"first_name": "John", "last_name": "Doe", "middle_name": "", "birth_date": ""}]
            return RecordCreator.build_record("username", "password", aliases)[0]
