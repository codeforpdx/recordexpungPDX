from html.parser import HTMLParser


class NodeParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.node_id = ''
        self.stop_flag = False

    def handle_starttag(self, tag, attrs):
        if not self.stop_flag and tag == 'option':
            self.node_id = dict(attrs)['value']
            self.stop_flag = True

    # TODO: Add error response here.
    def error(self, message):
        pass
