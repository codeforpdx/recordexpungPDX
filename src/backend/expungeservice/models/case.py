from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

from expungeservice.models.charge_types.charge import Charge


@dataclass
class Case:
    name: str
    birth_year: Optional[int]
    case_number: str
    citation_number: str
    location: str
    date: date
    violation_type: str
    current_status: str
    charges: List[Charge]
    case_detail_link: str
    __balance_due_in_cents: int = 0
    __probation_revoked: bool = False

    @staticmethod
    def create(info, case_number, citation_number, date_location, type_status,
               charges, case_detail_link, balance="0"):
        name = info[0]
        birth_year = Case._parse_birth_year(info)
        citation_number = citation_number[0] if citation_number else ""
        date, location = date_location
        date = datetime.date(datetime.strptime(date, '%m/%d/%Y'))
        violation_type, current_status = type_status
        case = Case(name, birth_year, case_number, citation_number, location,
                    date, violation_type, current_status, charges,
                    case_detail_link)
        case.set_balance_due(balance)
        return case

    def get_probation_revoked(self) -> bool:
        return self.__probation_revoked

    def set_probation_revoked(self, probation_revoked: bool):
        self.__probation_revoked = probation_revoked

    def set_balance_due(self, balance_due_dollar_amount):
        if type(balance_due_dollar_amount) == str:
            balance_due_dollar_amount = float(balance_due_dollar_amount.replace(',',''))
        self.__balance_due_in_cents = int(balance_due_dollar_amount * 100)

    def get_balance_due(self):
        return self.__balance_due_in_cents / 100

    def get_balance_due_in_cents(self):
        return self.__balance_due_in_cents

    def closed(self):
        if self._ignore_open_case():
            return True
        else:
            return self._closed()

    @staticmethod
    def _parse_birth_year(info) -> Optional[int]:
        if len(info) > 1:
            return int(info[1].split('/')[-1])
        else:
            return None

    def _ignore_open_case(self):
        return 'violation' in self.violation_type.lower() or 'municipal parking' == self.violation_type.lower()

    def _closed(self):
        return self.current_status == 'Closed' or self.current_status == 'Inactive' or self.current_status == 'Purgable'
