from concurrent.futures.thread import ThreadPoolExecutor
from copy import copy
from itertools import product
from typing import List

import requests
from datetime import datetime

from expungeservice.models.case import Case
from expungeservice.models.helpers.charge_creator import ChargeCreator
from expungeservice.models.disposition import Disposition
from expungeservice.crawler.parsers.param_parser import ParamParser
from expungeservice.crawler.parsers.node_parser import NodeParser
from expungeservice.crawler.parsers.record_parser import RecordParser
from expungeservice.crawler.parsers.case_parser import CaseParser
from expungeservice.crawler.request import *
from expungeservice.models.ambiguous import AmbiguousCharge, AmbiguousCase


class Crawler:
    def __init__(self):
        self.session = requests.Session()
        self.response = requests.Response()
        self.result = RecordParser()

    def login(self, username, password, close_session=False) -> bool:
        url = URL.login_url()
        payload = Payload.login_payload(username, password)

        self.response = self.session.post(url, data=payload)

        if close_session:
            self.session.close()

        return Crawler.__login_validation(self.response)

    def search(self, first_name, last_name, middle_name="", birth_date="") -> List[AmbiguousCase]:
        url = "https://publicaccess.courts.oregon.gov/PublicAccessLogin/Search.aspx?ID=100"
        node_response = self.__parse_nodes(url)
        payload = Crawler.__extract_payload(node_response, last_name, first_name, middle_name, birth_date)

        # perform search
        response = self.session.post(url, data=payload)
        self.result.feed(response.text)

        # Parse search results (case detail pages)
        with ThreadPoolExecutor(max_workers=50) as executor:
            ambiguous_cases = list(executor.map(self.__build_case, self.result.cases))
        self.session.close()
        return ambiguous_cases

    def __build_case(self, case) -> AmbiguousCase:
        case_parser_data = self.__parse_case(case)
        case.set_probation_revoked(case_parser_data.probation_revoked)
        case.set_balance_due(case_parser_data.balance_due)
        ambiguous_charges = []
        for charge_id, charge_dict in case_parser_data.hashed_charge_data.items():
            charge_dict["case"] = case
            ambiguous_charge = Crawler.__build_charge(charge_id, charge_dict, case_parser_data)
            ambiguous_charges.append(ambiguous_charge)
        ambiguous_case = []
        for i, charges in enumerate(product(*ambiguous_charges)):
            if i == 0:
                possible_case: Case = case  # TODO: Fix me. Hack to force case not be garbage collected
            else:
                possible_case: Case = copy(case)  # type: ignore
            possible_case.charges = list(charges)
            ambiguous_case.append(possible_case)
        return ambiguous_case

    def __parse_nodes(self, url):
        node_parser = NodeParser()
        node_parser.feed(self.response.text)
        payload = {"NodeID": node_parser.node_id, "NodeDesc": "All+Locations"}
        return self.session.post(url, data=payload)

    def __parse_case(self, case):
        response = self.session.get(case.case_detail_link)
        if response.status_code == 200 and response.text:
            return CaseParser.feed(response.text)
        else:
            raise ValueError(f"Failed to fetch case detail page. Please rerun the search.")

    @staticmethod
    def __extract_payload(node_response, last_name, first_name, middle_name, birth_date):
        param_parser = ParamParser()
        param_parser.feed(node_response.text)
        return Payload.payload(param_parser, last_name, first_name, middle_name, birth_date)

    @staticmethod
    def __login_validation(response):
        return "Case Records" in response.text

    @staticmethod
    def __build_charge(charge_id, charge, case_parser_data) -> AmbiguousCharge:
        if case_parser_data.hashed_dispo_data.get(charge_id):
            disposition_data = case_parser_data.hashed_dispo_data[charge_id]
            date = datetime.date(
                datetime.strptime(disposition_data.get("date"), "%m/%d/%Y")
            )  # TODO: Log error if format is not correct
            ruling = disposition_data.get("ruling")
            charge["disposition"] = Disposition(date, ruling, "amended" in disposition_data["event"].lower())
        return ChargeCreator.create(charge_id, **charge)
