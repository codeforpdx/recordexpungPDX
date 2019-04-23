import requests_mock
from expungeservice.crawler.crawler import Crawler
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe
from tests.fixtures.search_page_response import SearchPageResponse


class CrawlerFactory:

    @staticmethod
    def create_john_doe_default_record(crawler):
        base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
        with requests_mock.Mocker() as m:
            m.post(base_url + 'Search.aspx?ID=100', [{'text': SearchPageResponse.RESPONSE}, {'text': JohnDoe.RECORD}])

            base_url += 'CaseDetail.aspx'
            m.get(base_url + '?CaseID=X0001', text=CaseDetails.CASE_X1)
            m.get(base_url + '?CaseID=X0002', text=CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION)
            m.get(base_url + '?CaseID=X0003', text=CaseDetails.CASE_WITHOUT_DISPOS)

            crawler.search('John', 'Doe')

            return crawler

    @staticmethod
    def create_john_doe_single_record(crawler):
        base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
        with requests_mock.Mocker() as m:
            m.post(base_url + 'Search.aspx?ID=100', [{'text': SearchPageResponse.RESPONSE},
                                                     {'text': JohnDoe.SINGLE_CASE_RECORD}])
            base_url += 'CaseDetail.aspx'
            m.get(base_url + '?CaseID=CASEJD1', text=CaseDetails.CASEJD1)

            crawler.search('John', 'Doe')

            return crawler

    @staticmethod
    def create_blank_record(crawler):
        base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
        with requests_mock.Mocker() as m:
            m.post(base_url + 'Search.aspx?ID=100', [{'text': SearchPageResponse.RESPONSE},
                                                     {'text': JohnDoe.BLANK_RECORD}])
            crawler.search('John', 'Doe')

            return crawler
