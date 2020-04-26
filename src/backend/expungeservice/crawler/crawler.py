from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import replace
from functools import partial
from itertools import product
from typing import List, Tuple, Optional

from datetime import datetime

from expungeservice.charge_creator import ChargeCreator
from expungeservice.crawler.request import Payload, URL
from expungeservice.models.case import CaseCreator
from expungeservice.models.disposition import DispositionCreator
from expungeservice.crawler.parsers.param_parser import ParamParser
from expungeservice.crawler.parsers.node_parser import NodeParser
from expungeservice.crawler.parsers.record_parser import RecordParser
from expungeservice.crawler.parsers.case_parser import CaseParser
from expungeservice.models.ambiguous import AmbiguousCharge, AmbiguousCase
from expungeservice.models.record import Question


class InvalidOECIUsernamePassword(Exception):
    def __str__(self, *args, **kwargs):
        return "Invalid OECI username or password."


class OECIUnavailable(Exception):
    def __str__(self, *args, **kwargs):
        return """The eCourt site is offline during the 4th weekend of each month between 6 PM PST on Friday until noon on Sunday. During this time, record search will not function."""


class Crawler:
    @staticmethod
    def attempt_login(session, username, password) -> str:
        url = URL.login_url()
        payload = Payload.login_payload(username, password)
        response = session.post(url, data=payload)
        if Crawler._succeed_login(response):
            return response.text
        elif "Oregon eCourt is temporarily unavailable due to maintenance" in response.text:
            raise OECIUnavailable
        else:
            raise InvalidOECIUsernamePassword

    @staticmethod
    def search(
        session, login_response, first_name, last_name, middle_name="", birth_date=""
    ) -> Tuple[List[AmbiguousCase], List[Question]]:
        search_url = URL.search_url()
        node_response = Crawler._fetch_search_page(session, search_url, login_response)
        record = Crawler._search_record(
            session, node_response, search_url, first_name, last_name, middle_name, birth_date
        )
        case_limit = 300
        if len(record.cases) >= case_limit:
            raise ValueError(
                f"Found {len(record.cases)} matching cases, exceeding the limit of {case_limit}. Please add a date of birth to your search."
            )
        else:
            # Parse search results (case detail pages)
            with ThreadPoolExecutor(max_workers=50) as executor:
                ambiguous_cases: List[AmbiguousCase] = []
                questions_accumulator: List[Question] = []
                for ambiguous_case, questions in executor.map(partial(Crawler._build_case, session), record.cases):
                    ambiguous_cases.append(ambiguous_case)
                    questions_accumulator += questions
            return ambiguous_cases, questions_accumulator

    @staticmethod
    def _search_record(session, node_response, search_url, first_name, last_name, middle_name, birth_date):
        payload = Crawler.__extract_payload(node_response, last_name, first_name, middle_name, birth_date)
        response = session.post(search_url, data=payload)
        record_parser = RecordParser()
        record_parser.feed(response.text)
        return record_parser

    @staticmethod
    def _build_case(session, case) -> Tuple[AmbiguousCase, List[Question]]:
        case_parser_data = Crawler._parse_case(session, case)
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
            ambiguous_charge, question = Crawler._build_charge(charge_id, charge_dict, case_parser_data)
            ambiguous_charges.append(ambiguous_charge)
            if question:
                questions.append(question)
        ambiguous_case = []
        for charges in product(*ambiguous_charges):
            possible_case = replace(updated_case, charges=tuple(charges))
            ambiguous_case.append(possible_case)
        return ambiguous_case, questions

    @staticmethod
    def _fetch_search_page(session, url, login_response):
        node_parser = NodeParser()
        node_parser.feed(login_response)
        payload = {"NodeID": node_parser.node_id, "NodeDesc": "All+Locations"}
        return session.post(url, data=payload)

    @staticmethod
    def _parse_case(session, case):
        response = session.get(case.case_detail_link)
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
    def _succeed_login(response):
        return "Case Records" in response.text

    @staticmethod
    def _build_charge(charge_id, charge, case_parser_data) -> Tuple[AmbiguousCharge, Optional[Question]]:
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
