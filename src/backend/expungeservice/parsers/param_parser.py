from html.parser import HTMLParser


class ParamParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def error(self, message):
        pass