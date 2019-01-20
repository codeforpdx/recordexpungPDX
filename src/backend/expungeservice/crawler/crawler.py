import requests

from expungeservice.crawler.models.charge import Charge
from expungeservice.crawler.parsers.param_parser import ParamParser
from expungeservice.crawler.parsers.node_parser import NodeParser
from expungeservice.crawler.parsers.record_parser import RecordParser
from expungeservice.crawler.parsers.case_parser import CaseParser
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

    def search(self, first_name, last_name, middle_name='', birth_date=''):
        url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/Search.aspx?ID=100'
        node_response = self.__parse_nodes(url)
        payload = Crawler.__extract_payload(node_response, last_name, first_name, middle_name, birth_date)

        # perform search
        response = self.session.post(url, data=payload)
        self.result.feed(response.text)

        # Parse search results (case detail pages)
        for case in self.result.cases:
            case_parser = self.__parse_case(case)
            for charge_id, charge in case_parser.hashed_charge_data.items():
                new_charge = Crawler.__build_charge(charge_id, charge, case_parser)
                case.charges.append(new_charge)

        self.session.close()

    def __parse_nodes(self, url):
        node_parser = NodeParser()
        node_parser.feed(self.response.text)
        payload = {'NodeID': node_parser.node_id, 'NodeDesc': 'All+Locations'}
        return self.session.post(url, data=payload)

    def __parse_case(self, case):
        case_parser = CaseParser()
        response = self.session.get(case.case_detail_link)
        case_parser.feed(response.text)
        return case_parser

    @staticmethod
    def __extract_payload(node_response, last_name, first_name, middle_name, birth_date):
        param_parser = ParamParser()
        param_parser.feed(node_response.text)
        return Payload.payload(param_parser, last_name, first_name, middle_name, birth_date)

    @staticmethod
    def __login_validation(response, login_url):
        return response.url != login_url

    @staticmethod
    def __build_charge(charge_id, charge, case_parser):
        new_charge = Charge(**charge)
        if case_parser.hashed_dispo_data.get(charge_id):
            new_charge.disposition.date = case_parser.hashed_dispo_data[charge_id].get('date')
            new_charge.disposition.ruling = case_parser.hashed_dispo_data[charge_id].get('ruling')
        return new_charge
