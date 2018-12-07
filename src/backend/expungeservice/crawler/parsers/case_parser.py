import re

from html.parser import HTMLParser

from expungeservice.crawler.models.charge import Charge


class CaseParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.current_table_number = 0
        self.entering_table = False
        self.within_table_header = False

        self.collect_charge_info = False
        self.charge_table_data = []

        self.collect_event_table = False
        self.collect_dispo_header_date = False
        self.event_row = -1
        self.event_table_data = []

        self.balance_due = '0'
        self.collect_financial_info = False
        self.get_balance_due = False

        self.hashed_dispo_data = {}
        self.hashed_charge_data = {}

    def handle_starttag(self, tag, attrs):
        if CaseParser.__at_table_title(tag, attrs):
            self.entering_table = True
            self.current_table_number += 1
            self.within_table_header = True
            self.collect_charge_info = False
            self.collect_event_table = False
            self.collect_financial_info = False

        if self.collect_event_table:
            if tag == 'th':
                self.collect_dispo_header_date = True

        if self.collect_financial_info and tag == 'b':
            self.get_balance_due = True

    def handle_endtag(self, tag):
        charge_table = 2
        event_table = 3
        financial_table = 4

        if self.__exiting_table_header(tag):
            self.within_table_header = False
            if charge_table == self.current_table_number:
                self.collect_charge_info = True
            elif event_table == self.current_table_number:
                self.collect_event_table = True
            elif financial_table == self.current_table_number:
                self.collect_financial_info = True

        if tag == 'body':
            self.__format_dispo_data()
            self.__create_charge_hash()

    def handle_data(self, data):
        if self.entering_table:
            self.entering_table = False

        elif self.collect_charge_info:
            self.charge_table_data.append(data)

        elif self.collect_event_table:
            if self.collect_dispo_header_date:
                self.event_row += 1
                self.event_table_data.append([])
                self.event_table_data[self.event_row].append(data)
                self.collect_dispo_header_date = False

            else:
                self.event_table_data[self.event_row].append(data)

        elif self.get_balance_due:
            self.balance_due = data
            self.get_balance_due = False

    # TODO: Add error handling.
    def error(self, message):
        pass

    # Private methods

    @staticmethod
    def __at_table_title(tag, attrs):
        return tag == 'div' and dict(attrs).get('class') == 'ssCaseDetailSectionTitle'

    def __exiting_table_header(self, end_tag):
        return self.within_table_header and end_tag == 'tr'

    def __format_dispo_data(self):
        dispo_data = self.__filter_dispo_events()
        for dispo_row in dispo_data:
            start_index = 2
            if len(dispo_row[3].split('.\xa0')) == 2:
                start_index = 3

            while start_index < len(dispo_row) - 1:
                charge_id, charge = dispo_row[start_index].split('.\xa0')
                charge_id = int(charge_id)
                self.hashed_dispo_data[charge_id] = {}
                self.hashed_dispo_data[charge_id]['date'] = dispo_row[0]
                self.hashed_dispo_data[charge_id]['charge'] = charge
                self.hashed_dispo_data[charge_id]['ruling'] = dispo_row[start_index + 1]
                start_index += 2

    def __filter_dispo_events(self):
        dispo_list = []
        for event_row in self.event_table_data:
            if len(event_row) > 3 and event_row[3] == 'Disposition':
                dispo_list.append(event_row)

        result = []
        index = 0
        for dispo_row in dispo_list:
            result.append([])
            for data in dispo_row:
                if data != '\xa0':
                    result[index].append(data)
            index += 1

        return result

    def __create_charge_hash(self):
        index = 0
        while index < len(self.charge_table_data):
            charge_id = int(re.compile('\d*').match(self.charge_table_data[index]).group())
            self.hashed_charge_data[charge_id] = {}
            self.hashed_charge_data[charge_id]['name'] = self.charge_table_data[index + 1]
            self.hashed_charge_data[charge_id]['statute'] = self.charge_table_data[index + 2]
            self.hashed_charge_data[charge_id]['level'] = self.charge_table_data[index + 3]
            self.hashed_charge_data[charge_id]['date'] = self.charge_table_data[index + 4]
            index += 5
