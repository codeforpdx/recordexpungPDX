from datetime import datetime


class Case:

    def __init__(self, info, case_number, citation_number, date_location, type_status, charges, case_detail_link):
        self.name, birth_year = info
        self.birth_year = int(birth_year)
        self.case_number = case_number
        self.citation_number = citation_number[0] if citation_number else ""
        date, self.location = date_location
        self.date = datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        self.violation_type, self.current_status = type_status
        self.charges = charges
        self.case_detail_link = case_detail_link
