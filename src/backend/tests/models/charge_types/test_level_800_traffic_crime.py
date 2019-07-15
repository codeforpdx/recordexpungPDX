import unittest

from datetime import datetime, timedelta
from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestSingleChargeConvictions(unittest.TestCase):
    """
    Level 800 traffic charges expungeability are determined by the level of the charge and disposition.
    If the level contains the word violation then it is not expungeable (Violations are not type eligible).
    If the charge level is something other than a violation then it is type eligible.
    """

    def setUp(self):
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = ChargeFactory.build()
        self.convicted_disposition = {'ruling': 'Convicted', 'date': last_week}
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        charge.disposition = Disposition(**self.convicted_disposition)
        return charge

    def test_traffic_violation_min_statute(self):
        self.single_charge['statute'] = '801.000'
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.__class__.__name__ == 'Level800TrafficCrime'

    def test_traffic_violation_max_statute(self):
        self.single_charge['statute'] = '825.999'
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.__class__.__name__ == 'Level800TrafficCrime'

    def test_traffic_violation_801_000(self):
        self.single_charge['name'] = 'Traffic Violation'
        self.single_charge['statute'] = '801.000'
        self.single_charge['level'] = 'Class C Traffic Violation'
        traffic_violation_min = self.create_recent_charge()
        self.charges.append(traffic_violation_min)

        assert traffic_violation_min.expungement_result.type_eligibility is False
        assert traffic_violation_min.expungement_result.type_eligibility_reason == 'Ineligible under 137.225(5)'

    def test_traffic_violation_825_999(self):
        self.single_charge['name'] = 'Traffic Violation'
        self.single_charge['statute'] = '825.999'
        self.single_charge['level'] = 'Class C Traffic Violation'
        traffic_violation_max = self.create_recent_charge()
        self.charges.append(traffic_violation_max)

        assert traffic_violation_max.expungement_result.type_eligibility is False
        assert traffic_violation_max.expungement_result.type_eligibility_reason == 'Ineligible under 137.225(5)'
