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

from datetime import datetime, timedelta, date

from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.duii import Duii

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTestsParent

# TODO: we can separate these three types to different test files too.
class TestTrafficViolation(ChargeTypeTestsParent):
    def test_traffic_violation_min_statute(self):
        self.charge_dict["statute"] = "801.000"
        self.charge_dict["level"] = "Violation"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, TrafficViolation)

    def test_traffic_violation_max_statute(self):
        self.charge_dict["statute"] = "825.999"
        self.charge_dict["level"] = "Violation"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, TrafficViolation)

    def test_convicted_violation_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute="801.000", level="Class C Traffic Violation", disposition=self.convicted)

        assert isinstance(charge, TrafficViolation)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
        assert not charge.blocks_other_charges()

    def test_dismissed_violation_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute="801.000", level="Class C Traffic Violation", disposition=self.dismissed)

        assert isinstance(charge, TrafficViolation)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"
        assert not charge.blocks_other_charges()

    def test_convicted_infraction_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute="811135", level="Infraction Class B", disposition=self.convicted)

        assert isinstance(charge, TrafficViolation)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
        assert not charge.blocks_other_charges()

    def test_dismissed_infraction_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute="811135", level="Infraction Class B", disposition=self.dismissed)

        assert isinstance(charge, TrafficViolation)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"
        assert not charge.blocks_other_charges()

    def test_no_dispo_violation_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute="801.000", level="Class C Traffic Violation", disposition=None)
        charge.disposition = None

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            charge.expungement_result.type_eligibility.reason
            == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
        )
        assert not charge.blocks_other_charges()


class TestTrafficNonViolation(ChargeTypeTestsParent):
    """
    800 level misdemeanors and felonies are eligible Only If the case was dismissed
    """

    def test_misdemeanor_conviction_is_not_eligible(self):
        charge = ChargeFactory.create(statute="814.010(4)", level="Misdemeanor Class A", disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
        assert charge.blocks_other_charges()

    def test_misdemeanor_dismissal_is_eligible(self):
        charge = ChargeFactory.create(statute="814.010(4)", level="Misdemeanor Class A", disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"
        assert charge.blocks_other_charges()

    def test_felony_conviction_is_not_eligible(self):
        charge = ChargeFactory.create(statute="819.300", level="Felony Class C", disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(7)(a)"
        assert charge.blocks_other_charges()

    def test_felony_dismissal_is_eligible(self):
        charge = ChargeFactory.create(statute="819.300", level="Felony Class C", disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"
        assert charge.blocks_other_charges()


class TestDUII(ChargeTypeTestsParent):
    def test_duii(self):
        self.charge_dict["statute"] = "813.010"
        charge = self.create_recent_charge()

        assert isinstance(charge, Duii)
