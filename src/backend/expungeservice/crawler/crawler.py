from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import replace
from functools import partial
from typing import List

from datetime import datetime

from requests import Session

from expungeservice.crawler.request import Payload, URL
from expungeservice.models.case import CaseCreator, Case, OeciCase, CaseSummary
from expungeservice.models.charge import OeciCharge
from expungeservice.models.disposition import DispositionCreator
from expungeservice.crawler.parsers.param_parser import ParamParser
from expungeservice.crawler.parsers.node_parser import NodeParser
from expungeservice.crawler.parsers.record_parser import RecordParser
from expungeservice.crawler.parsers.case_parser import CaseParser


class InvalidOECIUsernamePassword(Exception):
    def __str__(self, *args, **kwargs):
        return "Invalid OECI username or password."


class OECIUnavailable(Exception):
    def __str__(self, *args, **kwargs):
        return """The eCourt site is offline during the 4th weekend of each month between 6 PM PST on Friday until noon on Sunday. During this time, record search will not function."""


class Crawler:
    @staticmethod
    def attempt_login(session: Session, username, password) -> str:
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
        session: Session, login_response, first_name, last_name, middle_name="", birth_date=""
    ) -> List[OeciCase]:
        search_url = URL.search_url()
        node_response = Crawler._fetch_search_page(session, search_url, login_response)
        oeci_search_result = Crawler._search_record(
            session, node_response, search_url, first_name, last_name, middle_name, birth_date
        )
        case_limit = 300
        if len(oeci_search_result.cases) >= case_limit:
            raise ValueError(
                f"Found {len(oeci_search_result.cases)} matching cases, exceeding the limit of {case_limit}. Please add a date of birth to your search."
            )
        else:
            # Parse search results (case detail pages)
            with ThreadPoolExecutor(max_workers=50) as executor:
                oeci_cases: List[OeciCase] = []
                for oeci_case in executor.map(partial(Crawler._read_case, session), oeci_search_result.cases):
                    oeci_cases.append(oeci_case)
            return oeci_cases

    @staticmethod
    def _search_record(session: Session, node_response, search_url, first_name, last_name, middle_name, birth_date):
        payload = Crawler.__extract_payload(node_response, last_name, first_name, middle_name, birth_date)
        response = session.post(search_url, data=payload)
        record_parser = RecordParser()
        record_parser.feed(response.text)
        return record_parser

    @staticmethod
    def _read_case(session: Session, case_summary: CaseSummary) -> OeciCase:
        case_parser_data = Crawler._parse_case(session, case_summary)
        balance_due_in_cents = CaseCreator.compute_balance_due_in_cents(case_parser_data.balance_due)
        probation_revoked = case_parser_data.probation_revoked
        charges: List[OeciCharge] = []
        for charge_id, charge_dict in case_parser_data.hashed_charge_data.items():
            charge = Crawler._build_oeci_charge(charge_id, charge_dict, case_parser_data)
            charges.append(charge)
        updated_case_summary = replace(
            case_summary, balance_due_in_cents=balance_due_in_cents, probation_revoked=probation_revoked
        )
        return OeciCase(updated_case_summary, charges=tuple(charges))

    @staticmethod
    def _fetch_search_page(session, url, login_response):
        node_parser = NodeParser()
        node_parser.feed(login_response)
        payload = {"NodeID": node_parser.node_id, "NodeDesc": "All+Locations"}
        return session.post(url, data=payload)

    @staticmethod
    def _parse_case(session: Session, case: CaseSummary):
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
    def _build_oeci_charge(charge_id, charge_dict, case_parser_data) -> OeciCharge:
        charge_dict["date"] = datetime.date(datetime.strptime(charge_dict["date"], "%m/%d/%Y"))
        if case_parser_data.hashed_dispo_data.get(charge_id):
            disposition = Crawler._build_disposition(case_parser_data, charge_id)
            return OeciCharge(charge_id, disposition=disposition, **charge_dict)
        else:
            return OeciCharge(charge_id, disposition=None, **charge_dict)

    @staticmethod
    def _build_disposition(case_parser_data, charge_id):
        disposition_data = case_parser_data.hashed_dispo_data[charge_id]
        date = datetime.date(
            datetime.strptime(disposition_data.get("date"), "%m/%d/%Y")
        )  # TODO: Log error if format is not correct
        ruling = disposition_data.get("ruling")
        disposition = DispositionCreator.create(date, ruling, "amended" in disposition_data["event"].lower())
        return disposition
