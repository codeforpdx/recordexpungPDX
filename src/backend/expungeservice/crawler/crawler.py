import requests

from expungeservice.crawler.parsers.record_parser import RecordParser
from expungeservice.crawler.request import *


class Crawler:

    def __init__(self):
        self.session = requests.Session()
        self.response = requests.Response
        self.result = RecordParser()

    def login(self, username, password):
        url = URL.login_url()
        payload = Payload.login_payload(username, password)

        self.response = self.session.post(url, data=payload)
        return Crawler.__login_validation(self.response, url)

    @staticmethod
    def __login_validation(response, login_url):
        return response.url != login_url
