class DefaultState:

    def __init__(self):
        self.read_table_title = True

    def store_data(self, case_parser, data):
        if self.read_table_title:
            case_parser.table_title = data
            self.read_table_title = False

    def check_tag(self, tag):
        pass
