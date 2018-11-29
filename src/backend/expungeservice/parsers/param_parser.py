from html.parser import HTMLParser


class ParamParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.event_target = ''
        self.event_argument = ''
        self.view_state = ''
        self.view_state_generator = ''
        self.event_validation = ''
        self.node_id = ''

    def handle_starttag(self, tag, attrs):
        """ Handle start tag

        Assigns the value of the input tag for the corresponding class attributes.

        :param tag: An html tag.
        :param attrs: A list of tuples of the tag's attributes.
        """
        if tag == 'input':
            switcher = {
                '__EVENTTARGET': self.__set_event_target,
                '__EVENTARGUMENT': self.__set_event_argument,
                '__VIEWSTATE': self.__set_view_state,
                '__VIEWSTATEGENERATOR': self.__set_view_state_generator,
                '__EVENTVALIDATION': self.__set_event_validation,
                'NodeID': self.__set_node_id
            }
            switcher.get(dict(attrs)['name'], self.__default)(dict(attrs).get('value'))

    # TODO: Add error handling.
    def error(self, message):
        pass

    # Private functions
    def __set_event_target(self, value):
        self.event_target = value

    def __set_event_argument(self, value):
        self.event_argument = value

    def __set_view_state(self, value):
        self.view_state = value

    def __set_view_state_generator(self, value):
        self.view_state_generator = value

    def __set_event_validation(self, value):
        self.event_validation = value

    def __set_node_id(self, value):
        self.node_id = value

    def __default(self, value):
        pass
