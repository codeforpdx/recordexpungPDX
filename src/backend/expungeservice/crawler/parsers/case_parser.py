import re
from typing import List, Dict

from bs4 import BeautifulSoup
from more_itertools import split_at

from expungeservice.crawler.fuzzy_search import FuzzySearch

SECTION_TITLE_CLASS = "ssCaseDetailSectionTitle"

PROBATION_REVOKED_SEARCH_TERMS = ["probation revoked", "prob revoked"]
EVENTS_TO_EXCLUDE = ["", "dispositions"]

class CaseParser:
    def __init__(self):
        self.event_table_data = []

        self.balance_due = "0"
        self.hashed_dispo_data = {}
        self.hashed_charge_data = {}

        self.probation_revoked = False

    def feed(self, data):
        soup = BeautifulSoup(data, "html.parser")
        self.hashed_charge_data = CaseParser.__build_charge_table_data(soup)
        self.__build_event_table_data(soup)
        self.__build_balance_due(soup)

        self.__format_dispo_data()

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

    def __build_event_table_data(self, soup):
        disposition_events = CaseParser.__parse_disposition_events(soup)
        for event in disposition_events:
            if CaseParser.__valid_event_table(event):
                event_parse = CaseParser.__parse_event_table(event)
                self.event_table_data.append(event_parse)

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

    # While this function can be taken care with `__parse_string_list`,
    # the named variables will become useful in the future.
    @staticmethod
    def __parse_event_table(event) -> List[str]:
        event_parts = event.contents
        assert len(event_parts) == 4
        date, empty_one, empty_two, event_table_wrapper = event_parts
        event_table = event_table_wrapper.contents
        if len(event_table) == 1:
            event_table_contents = event_table[0].contents
            if len(event_table_contents) == 5:
                event_type, officer, _, event_inner_table_div, created = event_table_contents
                event_inner_table_parse = CaseParser.__parse_string_list(event_inner_table_div)
                event_parse = [event_type.string, officer.string, *event_inner_table_parse, created.string,]
            elif len(event_table_contents) == 4:
                event_type, _, event_inner_table_div, created = event_table_contents
                event_inner_table_parse = CaseParser.__parse_string_list(event_inner_table_div)
                event_parse = [event_type.string, *event_inner_table_parse, created.string,]
            else:
                raise ValueError("len(event_table_contents) should always be 4 or 5.")
        else:
            raise ValueError("event_table should never be empty.")
        return [date.string, empty_one.string, empty_two.string, *event_parse]

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

    def __format_dispo_data(self):
        dispo_data = self.__filter_dispo_events()
        for dispo_row in dispo_data:
            start_index = 2
            if len(dispo_row[3].split(".\xa0")) == 2:
                start_index = 3

            while start_index < len(dispo_row) - 1:
                if CaseParser._valid_data(dispo_row[start_index].split(".\xa0")):
                    charge_id_string, charge = dispo_row[start_index].split(".\xa0")
                else:
                    start_index += 2
                    continue
                charge_id = int(charge_id_string)
                self.hashed_dispo_data[charge_id] = {}
                self.hashed_dispo_data[charge_id]["date"] = dispo_row[0]
                self.hashed_dispo_data[charge_id]["charge"] = charge
                self.hashed_dispo_data[charge_id]["ruling"] = dispo_row[start_index + 1]
                start_index += 2

    def __filter_dispo_events(self) -> List[List[str]]:
        dispo_list: List[str] = []
        for event_row in self.event_table_data:
            if len(event_row) > 3 and event_row[3] == "Disposition":
                dispo_list.append(event_row)

        result: List[List[str]] = []
        index = 0
        for dispo_row in dispo_list:
            result.append([])
            for data in dispo_row:
                if data != "\xa0":
                    result[index].append(data)
            index += 1

        return result

    @staticmethod
    def _valid_data(disposition):
        return len(disposition) == 2
