from datetime import datetime


class Case:

    def __init__(self, info, case_number, citation_number, date_location, type_status, charges, case_detail_link):
        self.name = info[0]
        self.birth_year = self._set_birth_year(info)
        self.case_number = case_number
        self.citation_number = citation_number[0] if citation_number else ""
        date, self.location = date_location
        self.date = datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        self.violation_type, self.current_status = type_status
        self.charges = charges
        self.balance_due_in_cents = 0
        self.case_detail_link = case_detail_link

    def set_balance_due(self, balance_due_dollar_amount):
        if type(balance_due_dollar_amount) == str:
            balance_due_dollar_amount = float(balance_due_dollar_amount.replace(',',''))
        self.balance_due_in_cents = int(balance_due_dollar_amount * 100)

    def get_balance_due(self):
        return self.balance_due_in_cents / 100

    def closed(self):
        if self._ignore_open_case():
            return True
        else:
            return self._closed()

    @staticmethod
    def _set_birth_year(info):
        if len(info) > 1:
            return int(info[1].split('/')[-1])
        else:
            return ''

    def _ignore_open_case(self):
        return 'violation' in self.violation_type.lower() or 'municipal parking' == self.violation_type.lower() 

    def _closed(self):
        return self.current_status == 'Closed' or self.current_status == 'Inactive' or self.current_status =='Purgable'
