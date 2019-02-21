from expungeservice.crawler.parsers.case_parser.default_state import DefaultState


class FinancialTableData:

    def store_data(self, case_parser, data):
        case_parser.balance_due = data
        case_parser.current_parser_state = DefaultState()
