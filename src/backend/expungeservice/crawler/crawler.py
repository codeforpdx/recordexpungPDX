from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import replace
from itertools import product
from typing import List, Tuple, Optional

import requests
from datetime import datetime

from expungeservice.charge_creator import ChargeCreator
from expungeservice.models.case import CaseCreator
from expungeservice.models.disposition import Disposition, DispositionCreator
from expungeservice.crawler.parsers.param_parser import ParamParser
from expungeservice.crawler.parsers.node_parser import NodeParser
from expungeservice.crawler.parsers.record_parser import RecordParser
from expungeservice.crawler.parsers.case_parser import CaseParser
from expungeservice.crawler.request import *
from expungeservice.models.ambiguous import AmbiguousCharge, AmbiguousCase
from expungeservice.models.record import Question


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

    def search(
        self, first_name, last_name, middle_name="", birth_date=""
    ) -> Tuple[List[AmbiguousCase], List[Question]]:
        url = "https://publicaccess.courts.oregon.gov/PublicAccessLogin/Search.aspx?ID=100"
        node_response = self.__parse_nodes(url)
        payload = Crawler.__extract_payload(node_response, last_name, first_name, middle_name, birth_date)

        # perform search
        response = self.session.post(url, data=payload)
        self.result.feed(response.text)

        case_limit = 300
        if len(self.result.cases) >= case_limit:
            raise ValueError(
                f"Found {len(self.result.cases)} matching cases, exceeding the limit of {case_limit}. Please add a date of birth to your search."
            )
        else:
            # Parse search results (case detail pages)
            with ThreadPoolExecutor(max_workers=50) as executor:
                ambiguous_cases: List[AmbiguousCase] = []
                questions_accumulator: List[Question] = []
                for ambiguous_case, questions in executor.map(self.__build_case, self.result.cases):
                    ambiguous_cases.append(ambiguous_case)
                    questions_accumulator += questions
            self.session.close()
            return ambiguous_cases, questions_accumulator

    def __build_case(self, case) -> Tuple[AmbiguousCase, List[Question]]:
        case_parser_data = self.__parse_case(case)
        balance_due_in_cents = CaseCreator.compute_balance_due_in_cents(case_parser_data.balance_due)
        updated_case = replace(
            case, balance_due_in_cents=balance_due_in_cents, probation_revoked=case_parser_data.probation_revoked
        )
        ambiguous_charges: List[AmbiguousCharge] = []
        questions: List[Question] = []
        for charge_id, charge_dict in case_parser_data.hashed_charge_data.items():
            charge_dict["case_number"] = updated_case.case_number
            charge_dict["violation_type"] = updated_case.violation_type
            charge_dict["birth_year"] = updated_case.birth_year
            ambiguous_charge, question = Crawler.__build_charge(charge_id, charge_dict, case_parser_data)
            ambiguous_charges.append(ambiguous_charge)
            if question:
                questions.append(question)
        ambiguous_case = []
        for charges in product(*ambiguous_charges):
            possible_case = replace(updated_case, charges=tuple(charges))
            ambiguous_case.append(possible_case)
        return ambiguous_case, questions

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
    def __build_charge(charge_id, charge, case_parser_data) -> Tuple[AmbiguousCharge, Optional[Question]]:
        if case_parser_data.hashed_dispo_data.get(charge_id):
            disposition_data = case_parser_data.hashed_dispo_data[charge_id]
            date = datetime.date(
                datetime.strptime(disposition_data.get("date"), "%m/%d/%Y")
            )  # TODO: Log error if format is not correct
            ruling = disposition_data.get("ruling")
            charge["disposition"] = DispositionCreator.create(
                date, ruling, "amended" in disposition_data["event"].lower()
            )
        return ChargeCreator.create(charge_id, **charge)
