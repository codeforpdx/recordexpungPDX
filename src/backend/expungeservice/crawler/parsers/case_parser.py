import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from bs4 import BeautifulSoup
from more_itertools import split_at

from expungeservice.util import DateWithFuture as date
from expungeservice.crawler.fuzzy_search import FuzzySearch

SECTION_TITLE_CLASS = "ssCaseDetailSectionTitle"

PROBATION_REVOKED_SEARCH_TERMS = ["probation revoked", "prob revoked"]
EVENTS_TO_EXCLUDE = ["", "dispositions"]


@dataclass
class CaseParserData:
    district_attorney_number: str
    sid: str
    hashed_charge_data: Dict[int, Dict[str, str]]
    hashed_dispo_data: Dict[int, Dict[str, str]]
    balance_due: str
    restitution: bool
    probation_revoked: Optional[date]


class CaseParser:
    @staticmethod
    def feed(data) -> CaseParserData:
        soup = BeautifulSoup(data, "html.parser")
        district_attorney_number = CaseParser.__parse_district_attorney_number(soup)
        sid = CaseParser.__parse_sid(soup)
        hashed_charge_data = CaseParser.__build_charge_table_data(soup)
        (
            hashed_dispo_data,
            probation_revoked_date_string,
        ) = CaseParser.__build_hashed_dispo_data_and_probation_revoked(soup)
        balance_due = CaseParser.__build_balance_due(soup)
        if probation_revoked_date_string:
            probation_revoked = date.fromdatetime(datetime.strptime(probation_revoked_date_string, "%m/%d/%Y"))
        else:
            probation_revoked = None  # type: ignore
        restitution = "restitution" in soup.text.lower()
        return CaseParserData(
            district_attorney_number, sid, hashed_charge_data, hashed_dispo_data, balance_due, restitution, probation_revoked
        )

    @staticmethod
    def __parse_district_attorney_number(soup) -> str:
        DISTRICT_ATTORNEY_KEY = "District Attorney Number:"
        labels = soup.find_all("th", "ssTableHeaderLabel", limit=10)
        table = {tag.string: tag.parent.find("td").string for tag in labels}
        return table.get(DISTRICT_ATTORNEY_KEY, "")

    @staticmethod
    def __parse_sid(soup) -> str:
        sid = CaseParser.__attempt_parse_sid(soup)
        if sid and isinstance(sid, str) and re.match("^[\w-]+$", sid):
            return sid
        else:
            return ""

    @staticmethod
    def __attempt_parse_sid(soup) -> str:
        try:
            party_information = soup.find("div", class_=SECTION_TITLE_CLASS, string="Party Information")
            for information_section in party_information.parent.next_siblings:
                sid_text = information_section.find(text=re.compile("SID"))
                if sid_text:
                    return sid_text.parent.next_sibling
            return ""
        except Exception:
            return ""

    @staticmethod
    def __build_charge_table_data(soup) -> Dict[int, Dict[str, str]]:
        hashed_charge_data = {}
        charge_information = soup.find("div", class_=SECTION_TITLE_CLASS, string="Charge Information")
        for charge_row in charge_information.parent.next_siblings:
            charge_row_tds = charge_row.findAll("td")
            cells = [cell.text for cell in charge_row_tds if len(cell.text.replace("\xa0", "")) != 0]
            if len(cells) > 0:
                charge_id_string = cells[0]
                charge_id_match = re.compile("\d*").match(charge_id_string)
                if charge_id_match:
                    charge_id = int(charge_id_match.group())
                    charge_data = {"name": cells[1], "statute": cells[2], "level": cells[3], "date": cells[4]}
                    hashed_charge_data[charge_id] = charge_data
                else:
                    raise ValueError(f"Could not parse charge id from {charge_id_string}.")
        return hashed_charge_data

    # Note that one disposition event may have rulings for one or more charges
    # and thus the accumulator pattern.
    @staticmethod
    def __build_hashed_dispo_data_and_probation_revoked(soup) -> Tuple[Dict[int, Dict[str, str]], Optional[str]]:
        disposition_events, other_events = CaseParser.__parse_events(soup)
        acc: Dict[int, Dict[str, str]] = {}
        for event in disposition_events:
            if CaseParser.__valid_event_table(event):
                disposition_data = CaseParser.__parse_event_table(event)
                if disposition_data:
                    acc = {**acc, **disposition_data}
        latest_probation_revoked_date = None
        for event in other_events:
            if CaseParser.__valid_event_table(event):
                probation_revoked_date = CaseParser.__parse_probation_revoked(event)
                if probation_revoked_date:
                    latest_probation_revoked_date = probation_revoked_date
        return acc, latest_probation_revoked_date

    @staticmethod
    def __parse_probation_revoked(event):
        event_parts = event.contents
        assert len(event_parts) == 4
        date, empty_one, empty_two, event_table_wrapper = event_parts
        if FuzzySearch.search(event_table_wrapper.text, PROBATION_REVOKED_SEARCH_TERMS):
            return date.text

    @staticmethod
    def __parse_events(soup):
        events_title = soup.find("div", class_=SECTION_TITLE_CLASS, string="Events & Orders of the Court")
        events = list(events_title.parent.next_siblings)
        split_events = list(split_at(events, CaseParser.__is_other_events_and_hearings))
        assert len(split_events) == 2
        return split_events

    @staticmethod
    def __is_other_events_and_hearings(event):
        return CaseParser.__normalize_text(event.text) == "other events and hearings".replace(" ", "")

    @staticmethod
    def __build_balance_due(soup) -> str:
        financial_information = soup.find("div", class_=SECTION_TITLE_CLASS, string="Financial Information")
        if financial_information:
            return financial_information.parent.parent.find("b").text
        else:
            return "0"

    @staticmethod
    def __normalize_text(text):
        return text.replace("\xa0", "").replace(" ", "").lower()

    @staticmethod
    def __valid_event_table(event):
        return not CaseParser.__normalize_text(event.text) in EVENTS_TO_EXCLUDE

    @staticmethod
    def __parse_event_table(event) -> Optional[Dict[int, Dict[str, str]]]:
        event_parts = event.contents
        assert len(event_parts) == 4
        date, empty_one, empty_two, event_table_wrapper = event_parts
        event_table = event_table_wrapper.contents
        if len(event_table) == 1:
            event_table_contents = event_table[0].contents
            if len(event_table_contents) >= 5 and len(event_table_contents) % 2 == 1:
                event_type, officer, _, event_inner_table_div, created, *rest = event_table_contents
                event_inner_table_parse = CaseParser.__parse_string_list(event_inner_table_div)
            elif len(event_table_contents) >= 4 and len(event_table_contents) % 2 == 0:
                event_type, _, event_inner_table_div, created, *rest = event_table_contents
                event_inner_table_parse = CaseParser.__parse_string_list(event_inner_table_div)
            else:
                raise ValueError("len(event_table_contents) should always be greater than 3.")

            if CaseParser.__normalize_text(event_type.text) in ["disposition", "amendeddisposition"]:
                disposition_data = {}
                for row, next_row in zip(event_inner_table_parse, event_inner_table_parse[1:]):
                    if CaseParser._valid_data(row.split(".\xa0")):
                        charge_id_string, charge = row.split(".\xa0")
                        charge_id = int(charge_id_string)
                        disposition_data[charge_id] = {
                            "date": str(date.text),
                            "charge": str(charge),
                            "ruling": str(next_row),
                            "event": str(event_type.text),
                        }
                return disposition_data
            else:
                return None
        else:
            raise ValueError("event_table should never be empty.")

    @staticmethod
    def __parse_string_list(content) -> List[str]:
        if content:
            if isinstance(content, str):
                return [content]
            else:
                string_list = []
                for e in content.contents:
                    string_list.extend(CaseParser.__parse_string_list(e))
                return string_list
        else:
            return []

    @staticmethod
    def _valid_data(disposition):
        return len(disposition) == 2
