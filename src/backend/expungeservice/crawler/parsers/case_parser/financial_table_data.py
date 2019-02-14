class FinancialTableData:

    def store_data(self, case_parser, data):
        case_parser.balance_due = data
        case_parser.get_balance_due = False
