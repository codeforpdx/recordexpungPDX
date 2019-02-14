class EventTableData:
    def store_data(self, case_parser, data):
        if case_parser.collect_dispo_header_date:
            case_parser.event_row += 1
            case_parser.event_table_data.append([])
            case_parser.event_table_data[case_parser.event_row].append(data)
            case_parser.collect_dispo_header_date = False

        else:
            case_parser.event_table_data[case_parser.event_row].append(data)
