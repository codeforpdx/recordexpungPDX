class ChargeTableData:

    def __init__(self):
        self.data_tag = False

    def store_data(self, case_parser, data):
        if self.data_tag and data != '\xa0':
            case_parser.charge_table_data.append(data)

    def check_tag(self, tag, attrs):
        if tag == 'td':
            self.data_tag = True
        else:
            self.data_tag = False
