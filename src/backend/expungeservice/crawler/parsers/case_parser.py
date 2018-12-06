from html.parser import HTMLParser

from expungeservice.crawler.models.charge import Charge


class CaseParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.charges = []
        self.current_table_number = 0
        self.entering_table = False
        self.within_table_header = False

        self.collect_charge_info = False
        self.charge_table_data = []

        self.collect_disposition_table = False
        self.collect_dispo_header_date = False
        self.disposition_row = -1
        self.disposition_table_data = []

    def handle_starttag(self, tag, attrs):
        if CaseParser.__at_table_title(tag, attrs):
            self.entering_table = True
            self.current_table_number += 1
            self.within_table_header = True
            self.collect_disposition_table = False

        if self.collect_disposition_table:
            if tag == 'th':
                self.collect_dispo_header_date = True

    def handle_endtag(self, tag):
        charge_table = 2
        disposition_table = 3

        if self.__exiting_table_header(tag):
            self.within_table_header = False
            if charge_table == self.current_table_number:
                self.collect_charge_info = True
            elif disposition_table == self.current_table_number:
                self.collect_disposition_table = True

        if tag == 'table':
            self.collect_charge_info = False

    def handle_data(self, data):
        if self.entering_table:
            self.entering_table = False

        elif self.collect_charge_info:
            self.charge_table_data.append(data)

        elif self.collect_disposition_table:
            if self.collect_dispo_header_date:
                self.disposition_row += 1
                self.disposition_table_data.append([])
                self.disposition_table_data[self.disposition_row].append(data)
                self.collect_dispo_header_date = False

            else:
                self.disposition_table_data[self.disposition_row].append(data)

    # TODO: Add error handling.
    def error(self, message):
        pass

    # Private methods

    @staticmethod
    def __at_table_title(tag, attrs):
        return tag == 'div' and dict(attrs).get('class') == 'ssCaseDetailSectionTitle'

    def __exiting_table_header(self, end_tag):
        return self.within_table_header and end_tag == 'tr'
