from html.parser import HTMLParser

from expungeservice.crawler.models.charge import Charge


class CaseParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.charges = []
        self.current_table_number = 0
        self.entering_table = False
        self.within_table_header = False

    def handle_starttag(self, tag, attrs):
        if CaseParser.__at_table_title(tag, attrs):
            self.entering_table = True
            self.current_table_number += 1
            self.within_table_header = True

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    # TODO: Add error handling.
    def error(self, message):
        pass

    # Private methods

    @staticmethod
    def __at_table_title(tag, attrs):
        return tag == 'div' and dict(attrs).get('class') == 'ssCaseDetailSectionTitle'
