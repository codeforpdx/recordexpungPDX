import re
from typing import List

from bs4 import BeautifulSoup

from expungeservice.crawler.fuzzy_search import FuzzySearch

SECTION_TITLE_CLASS = "ssCaseDetailSectionTitle"

PROBATION_REVOKED_SEARCH_TERMS = ["probation revoked", "prob revoked"]
EVENTS_TO_EXCLUDE = ["", "dispositions", "other events and hearings".replace(" ", "")]

class CaseParser:
    def __init__(self):
        self.charge_table_data = []
        self.event_table_data = []

        self.balance_due = "0"
        self.hashed_dispo_data = {}
        self.hashed_charge_data = {}

        self.probation_revoked = False

    def feed(self, data):
        soup = BeautifulSoup(data, "html.parser")
        self.__build_charge_table_data(soup)
        self.__build_event_table_data(soup)
        self.__build_balance_due(soup)

        self.__format_dispo_data()
        self.__create_charge_hash()

        self.probation_revoked = FuzzySearch.search(data, PROBATION_REVOKED_SEARCH_TERMS)

    def __build_charge_table_data(self, soup):
        charge_information = soup.find("div", class_=SECTION_TITLE_CLASS, string="Charge Information")
        for row in charge_information.parent.next_siblings:
            for cell in row.findAll("td"):
                if len(cell.text.replace("\xa0", "")) != 0:
                    self.charge_table_data.append(cell.text)

    def __build_event_table_data(self, soup):
        events = soup.find("div", class_=SECTION_TITLE_CLASS, string="Events & Orders of the Court")
        for event in events.parent.next_siblings:
            # TODO: Remove this first case; I inserted this in to preserve legacy behavior.
            if event.text.replace("\xa0", "") == "OTHER EVENTS AND HEARINGS":
                self.event_table_data.append(["OTHER EVENTS AND HEARINGS"])
            elif CaseParser.__valid_event_table(event):
                event_parse = CaseParser.__parse_event_table(event)
                self.event_table_data.append(event_parse)

    def __build_balance_due(self, soup):
        financial_information = soup.find("div", class_=SECTION_TITLE_CLASS, string="Financial Information")
        if financial_information:
            self.balance_due = financial_information.parent.parent.find("b").text

    @staticmethod
    def __valid_event_table(event):
        return not event.text.replace("\xa0", "").replace(" ", "").lower() in EVENTS_TO_EXCLUDE

    # While this function can be taken care with `__parse_string_list`,
    # the named variables will become useful in the future.
    @staticmethod
    def __parse_event_table(event) -> List[str]:
        event_parts = event.contents
        assert len(event_parts) == 4
        date, empty_one, empty_two, event_table_wrapper = event_parts
        event_table = event_table_wrapper.contents
        if len(event_table) > 1:
            # With link
            event_parse = CaseParser.__parse_string_list(event_table_wrapper)
        elif len(event_table) == 1:
            # Without link
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

    def __create_charge_hash(self):
        index = 0
        while index < len(self.charge_table_data):
            charge_id_match = re.compile("\d*").match(self.charge_table_data[index])
            if charge_id_match:
                charge_id = int(charge_id_match.group())
                self.hashed_charge_data[charge_id] = {}
                self.hashed_charge_data[charge_id]["name"] = self.charge_table_data[index + 1]
                self.hashed_charge_data[charge_id]["statute"] = self.charge_table_data[index + 2]
                self.hashed_charge_data[charge_id]["level"] = self.charge_table_data[index + 3]
                self.hashed_charge_data[charge_id]["date"] = self.charge_table_data[index + 4]
                index += 5
            else:
                raise ValueError(f"Could not find charge id at {index} of charge table data.")

    @staticmethod
    def _valid_data(disposition):
        return len(disposition) == 2
