from expungeservice.expunger.helper_functions import *
import datetime
import enum

CaseState = enum.Enum('CaseState', 'OPEN CLOSED')

class Case:

    def __init__(self, info, case_number, citation_number, date_location, type_status, charges, case_detail_link, state=None, balance_due=0.0):
        self.name, birth_year = info
        self.birth_year = date2obj(birth_year)
        self.case_number = case_number
        self.citation_number = citation_number[0] if citation_number else ""
        self.date, self.location = date_location #todo: clean this up  and put stuff in the parser

        self.date = date2obj(self.date)

        self.violation_type, self.current_status = type_status
        self.charges = charges
        self.case_detail_link = case_detail_link
        self.state = state

        self.balance_due = balance_due

    def setCharges(self, charges): #this function exists to update the charges with more details
        self.charges = charges

    def num_charges(self):
         return len(self.charges)

    def set_state(self, state): #todo: less ambiguous name
        self.state = state

    def __dict__(self):

        charge_list =[]

        for charge in self.charges:
            charge_list.append(charge.__dict__())

        return {'name': self.name,
                'birth_year': str(self.birth_year),
                'case_number': self.case_number,
                'citation_number': self.citation_number,
                'date': str(self.date),
                'violation_type': self.violation_type,
                'current_status': self.current_status,
                'charges': charge_list,
                'case_detail_link': self.case_detail_link,
                'state': self.state,
                'balance_due': self.balance_due}