from datetime import date as date_class
from expungeservice.models.charge import Charge
from tests.factories.case_factory import CaseFactory


class ChargeFactory:

    @staticmethod
    def build():
        return {
                  'case': CaseFactory.create(),
                  'name': 'Theft of services',
                  'statute': '164.125',
                  'level': 'Misdemeanor Class A',
                  'date': '1/1/0001'
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
        kwargs = {'case': case, 'name': name, 'statute': statute, 'level': level, 'date': date}
        charge = Charge.create(**kwargs)
        if disposition:
            charge.disposition.ruling, charge.disposition.date = disposition

        return charge

    @staticmethod
    def create_dismissed_charge(case=CaseFactory.create(),
                                name='Theft of services',
                                statute='164.125',
                                level='Misdemeanor Class A',
                                date='1/1/0001'):
        kwargs = {'case': case, 'name': name, 'statute': statute, 'level': level, 'date': date}
        charge = Charge.create(**kwargs)
        charge.disposition.ruling, charge.disposition.date = ['Dismissed', date_class.today()]

        return charge
