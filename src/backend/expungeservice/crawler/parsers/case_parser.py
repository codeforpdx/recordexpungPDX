import re
from typing import List, Dict, Tuple, Optional

from bs4 import BeautifulSoup
from more_itertools import split_at

from expungeservice.crawler.fuzzy_search import FuzzySearch

SECTION_TITLE_CLASS = "ssCaseDetailSectionTitle"

PROBATION_REVOKED_SEARCH_TERMS = ["probation revoked", "prob revoked"]
EVENTS_TO_EXCLUDE = ["", "dispositions"]

class CaseParser:
    def __init__(self):
        self.balance_due = "0"
        self.hashed_dispo_data = {}
        self.hashed_charge_data = {}

        self.probation_revoked = False

    def feed(self, data):
        soup = BeautifulSoup(data, "html.parser")
        self.hashed_charge_data = CaseParser.__build_charge_table_data(soup)
        self.hashed_dispo_data = CaseParser.__build_hashed_dispo_data(soup)
        self.__build_balance_due(soup)

        self.probation_revoked = FuzzySearch.search(data, PROBATION_REVOKED_SEARCH_TERMS)

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
    def __build_hashed_dispo_data(soup):
        disposition_events = CaseParser.__parse_disposition_events(soup)
        acc: Dict[int, Dict[str, str]] = {}
        for event in disposition_events:
            if CaseParser.__valid_event_table(event):
                disposition_data = CaseParser.__parse_event_table(event)
                if disposition_data:
                    acc = {**acc, **disposition_data}
        return acc

    @staticmethod
    def __parse_disposition_events(soup):
        events_title = soup.find("div", class_=SECTION_TITLE_CLASS, string="Events & Orders of the Court")
        events = list(events_title.parent.next_siblings)
        split_events = list(split_at(events, CaseParser.__is_other_events_and_hearings))
        assert len(split_events) == 2
        disposition_events, other_events = split_events
        return disposition_events

    @staticmethod
    def __is_other_events_and_hearings(event):
        return CaseParser.__normalize_text(event.text) == "other events and hearings".replace(" ", "")

    def __build_balance_due(self, soup):
        financial_information = soup.find("div", class_=SECTION_TITLE_CLASS, string="Financial Information")
        if financial_information:
            self.balance_due = financial_information.parent.parent.find("b").text

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
            if len(event_table_contents) == 5:
                event_type, officer, _, event_inner_table_div, created = event_table_contents
                event_inner_table_parse = CaseParser.__parse_string_list(event_inner_table_div)
            elif len(event_table_contents) == 4:
                event_type, _, event_inner_table_div, created = event_table_contents
                event_inner_table_parse = CaseParser.__parse_string_list(event_inner_table_div)
            else:
                raise ValueError("len(event_table_contents) should always be 4 or 5.")

            if CaseParser.__normalize_text(event_type.text) == "disposition":
                disposition_data = {}
                for row, next_row in zip(event_inner_table_parse, event_inner_table_parse[1:]):
                    if CaseParser._valid_data(row.split(".\xa0")):
                        charge_id_string, charge = row.split(".\xa0")
                        charge_id = int(charge_id_string)
                        disposition_data[charge_id] = {"date": date.text, "charge": charge, "ruling": next_row}
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
