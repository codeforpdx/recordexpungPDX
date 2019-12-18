class EventTableData:
    
    def __init__(self):
        self._header_tag = 'th'
        self._dispo_header = False
        self._event_row = -1

    def store_data(self, case_parser, data):
        if self._dispo_header:
            self._event_row += 1
            case_parser.event_table_data.append([])
            case_parser.event_table_data[self._event_row].append(data)
            self._dispo_header = False

        else:
            case_parser.event_table_data[self._event_row].append(data)

    def check_tag(self, tag, attrs):
        if self._header_tag == tag and dict(attrs).get('class') in ['ssTableHeaderLabel', 'ssEventsAndOrdersSubTitle']:
            self._dispo_header = True
