"""
Rules for 800 Level charges are as follows:

800 level misdemeanors and felonies are eligible Only If the case was dismissed
800 level cases of any kind that are convicted are not eligible
800 level infractions do not block other cases
800 level misdemeanor and felony convictions do block
800 level misdemeanor and felony arrests block like other arrests
800 level convictions of any kind are not type eligible
"""

import unittest

from datetime import date, datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestTrafficViolation(unittest.TestCase):
    def setUp(self):
        self.single_charge = ChargeFactory.build()
        self.charges = []
        last_week = datetime.today() - timedelta(days=7)
        self.convicted = ["Convicted", last_week]
        self.dismissed = ["Dismissed", last_week]

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        last_week = datetime.today() - timedelta(days=7)
        charge.disposition = Disposition(ruling="Convicted", date=last_week)
        return charge

    def test_traffic_violation_min_statute(self):
        self.single_charge["statute"] = "801.000"
        self.single_charge["level"] = "Violation"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.__class__.__name__ == "TrafficViolation"
        assert charge.type_name == "Traffic Violation"

    def test_traffic_violation_max_statute(self):
        self.single_charge["statute"] = "825.999"
        self.single_charge["level"] = "Violation"

        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.__class__.__name__ == "TrafficViolation"

    def test_duii(self):
        self.single_charge["statute"] = "813.010"
        charge = self.create_recent_charge()

        assert charge.__class__.__name__ == "Duii"
        assert charge.type_name == "DUII"

    def test_convicted_violation_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute="801.000", level="Class C Traffic Violation", disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
        assert not charge.blocks_other_charges()

    def test_dismissed_violation_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute="801.000", level="Class C Traffic Violation", disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"
        assert not charge.blocks_other_charges()

    def test_convicted_infraction_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute="811135", level="Infraction Class B", disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
        assert not charge.blocks_other_charges()

    def test_dismissed_infraction_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute="811135", level="Infraction Class B", disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"
        assert not charge.blocks_other_charges()


class TestTrafficNonViolation(unittest.TestCase):
    """
    800 level misdemeanors and felonies are eligible Only If the case was dismissed
    """

    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.convicted = ["Convicted", last_week]
        self.dismissed = ["Dismissed", last_week]

    def test_misdemeanor_conviction_is_not_eligible(self):
        charge = ChargeFactory.create(statute="814.010(4)", level="Misdemeanor Class A", disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
        assert charge.blocks_other_charges()

    def test_misdemeanor_dismissal_is_eligible(self):
        charge = ChargeFactory.create(statute="814.010(4)", level="Misdemeanor Class A", disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Dismissal eligible under 137.225(1)(b)"
        assert charge.blocks_other_charges()

    def test_felony_conviction_is_not_eligible(self):
        charge = ChargeFactory.create(statute="819.300", level="Felony Class C", disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
        assert charge.blocks_other_charges()

    def test_felony_dismissal_is_eligible(self):
        charge = ChargeFactory.create(statute="819.300", level="Felony Class C", disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Dismissal eligible under 137.225(1)(b)"
        assert charge.blocks_other_charges()
