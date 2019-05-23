from html.parser import HTMLParser

from expungeservice.models.case import Case


class RecordParser(HTMLParser):
    BASE_URI = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'

    def __init__(self):
        HTMLParser.__init__(self)
        self.cases = []
        self.column = 0
        self.within_tr_tag = False
        self.within_nested_tr = False
        self.collect_data = False
        self.case_number = ''      # column 1
        self.citation_number = []  # column 2
        self.info = []             # column 3
        self.date_location = []    # column 4
        self.type_status = []      # column 5
        self.charges = []          # column 6+
        self.case_detail_link = ''

    def handle_starttag(self, tag, attrs):
        self.__increase_column_count(tag)
        if self.__case_column():
            self.__assign_case_link(tag, attrs)
        self.__set_flags(tag)

    def handle_endtag(self, tag):
        if self.__exiting_nested_table(tag):
            self.within_nested_tr = False
        elif self.__collect_tr_data(tag):
            if self.__valid_row():
                self.__record_case()
                self.__reset_case()
            self.__reset_flags()

    def handle_data(self, data):
        if self.__within_valid_table_row():
            switcher = {
                1: self.__set_case_number,
                2: self.__set_citation_number,
                3: self.__set_info,
                4: self.__set_date_location,
                5: self.__set_type_status,
            }
            switcher.get(self.column, self._set_charges)(data)

        elif 'Charge(s)' == data:
            self.collect_data = True

    # TODO: Add error response.
    def error(self, message):
        pass

    def __set_case_number(self, data):
        self.case_number = data

    def __set_citation_number(self, data):
        self.citation_number.append(data)

    def __set_info(self, data):
        self.info.append(data)

    def __set_date_location(self, data):
        self.date_location.append(data)

    def __set_type_status(self, data):
        self.type_status.append(data)

    def _set_charges(self, data):
        self.charges.append(data)

    def __record_case(self):
        self.cases.append(Case(self.info, self.case_number, self.citation_number, self.date_location,
                                    self.type_status, [], self.case_detail_link))

    def __reset_case(self):
        self.case_number = ''      # column 1
        self.citation_number = []  # column 2
        self.info = []             # column 3
        self.date_location = []    # column 4
        self.type_status = []      # column 5
        self.charges = []          # column 6+
        self.case_detail_link = ''

    def __valid_row(self):
        valid_length = 1
        return len(self.info) >= valid_length

    def __reset_flags(self):
        self.column = 0
        self.within_tr_tag = False

    def __increase_column_count(self, tag):
        if tag == 'td':
            self.column += 1

    def __case_column(self):
        return self.column == 1

    def __assign_case_link(self, tag, attrs):
        if tag == 'a' and self.collect_data:
            self.case_detail_link = self.BASE_URI + dict(attrs)['href']

    def __set_flags(self, tag):
        if self.__nested_table_row(tag):
            self.within_nested_tr = True
        elif self.__collect_tr_data(tag):
            self.within_tr_tag = True

    def __collect_tr_data(self, tag):
        return tag == 'tr' and self.collect_data

    def __nested_table_row(self, tag):
        return tag == 'tr' and self.within_tr_tag

    def __exiting_nested_table(self, tag):
        return tag == 'tr' and self.within_nested_tr

    def __within_valid_table_row(self):
        return self.within_tr_tag and self.collect_data
