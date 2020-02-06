import unittest
from datetime import date, datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition

class TestCivilOffense(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.convicted = ["Convicted", last_week]
        self.dismissed = ["Dismissed", last_week]

    def test_00_is_not_a_civil_offense(self):
        charge = ChargeFactory.create(statute="00", level="N/A", disposition=self.convicted)

        assert charge.__class__.__name__ != "CivilOffense"

    def test_100_is_not_a_civil_offense(self):
        charge = ChargeFactory.create(statute="100", level="N/A", disposition=self.convicted)

        assert charge.__class__.__name__ != "CivilOffense"

    def test_99_is_a_civil_offense(self):
        charge = ChargeFactory.create(statute="99", level="N/A", disposition=self.convicted)

        assert charge.__class__.__name__ == "CivilOffense"

    def test_55_is_a_civil_offense(self):
        charge = ChargeFactory.create(statute="55", level="N/A", disposition=self.convicted)

        assert charge.__class__.__name__ == "CivilOffense"

    def test_fugitive_complaint(self):
        charge = ChargeFactory.create(statute="0", level="N/A", name="Fugitive Complaint", disposition=self.convicted)

        assert charge.__class__.__name__ == "CivilOffense"
