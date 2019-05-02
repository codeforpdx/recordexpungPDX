from expungeservice.crawler.models.charge import Charge
from tests.factories.case_factory import CaseFactory


class ChargeFactory:

    @staticmethod
    def create(case=CaseFactory.create(),
               name='Theft of services',
               statute='164.125',
               level='Misdemeanor Class A',
               date='1/1/0001',
               disposition=None):
        charge = Charge(case, name, statute, level, date)
        if disposition:
            charge.disposition.ruling, charge.disposition.date = disposition

        return charge
