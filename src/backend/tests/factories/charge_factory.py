from datetime import date as date_class
from expungeservice.models.charge import Charge
from expungeservice.models.disposition import Disposition
from tests.factories.case_factory import CaseFactory


class ChargeFactory:

    @staticmethod
    def build(disposition=None):
        return {
                  'case': CaseFactory.create(),
                  'name': 'Theft of services',
                  'statute': '164.125',
                  'level': 'Misdemeanor Class A',
                  'date': '1/1/0001',
                  'disposition': disposition
                }

    @staticmethod
    def save(charge):
        return Charge.create(**charge)

    @staticmethod
    def create(case=CaseFactory.create(),
               name='Theft of services',
               statute='164.125',
               level='Misdemeanor Class A',
               date='1/1/0001',
               disposition=None):
        if disposition:
            ruling, date = disposition
            disposition = Disposition(date=date, ruling=ruling)
        kwargs = {'case': case, 'name': name, 'statute': statute, 'level': level, 'date': date, 'disposition': disposition}

        return Charge.create(**kwargs)

    @staticmethod
    def create_dismissed_charge(case=CaseFactory.create(),
                                name='Theft of services',
                                statute='164.125',
                                level='Misdemeanor Class A',
                                date='1/1/0001'):
        disposition = Disposition(date=date_class.today().strftime('%m/%d/%Y'), ruling='Dismissed')
        kwargs = {'case': case, 'name': name, 'statute': statute, 'level': level, 'date': date, 'disposition': disposition}

        return Charge.create(**kwargs)
