import requests_mock

from tests.fixtures.search_page_response import SearchPageResponse


class CrawlerFactory:

    @staticmethod
    def create(crawler, record, cases):
        base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'

        with requests_mock.Mocker() as m:
            m.post("{}{}".format(base_url, 'Search.aspx?ID=100'), [{'text': SearchPageResponse.RESPONSE},
                                                                   {'text': record}])

            for key, value in cases.items():
                m.get("{}{}{}".format(base_url, 'CaseDetail.aspx?CaseID=', key), text=value)

            crawler.search('John', 'Doe')
