from html.parser import HTMLParser

from expungeservice.crawler.models.charge import Charge


class CaseParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.charges = []

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    # TODO: Add error handling.
    def error(self, message):
        pass

