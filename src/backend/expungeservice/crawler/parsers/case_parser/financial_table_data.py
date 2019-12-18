class FinancialTableData:

    def __init__(self):
        self._balance_due_tag = 'b'
        self._parse_balance = False

    def store_data(self, case_parser, data):
        if self._parse_balance:
            case_parser.balance_due = data
            self._parse_balance = False

    def check_tag(self, tag, attrs):
        if tag == self._balance_due_tag:
            self._parse_balance = True
