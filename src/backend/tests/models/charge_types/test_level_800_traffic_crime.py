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

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestLevel800Charges(unittest.TestCase):

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


class TestLevel800MisdemeanorFelonyEligibility(unittest.TestCase):
    """
    800 level misdemeanors and felonies are eligible Only If the case was dismissed
    """

    def setUp(self):
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.convicted = ['Convicted', last_week]
        self.dismissed= ['Dismissed', last_week]

    def test_misdemeanor_conviction_is_not_eligible(self):
        charge = ChargeFactory.create(statute='813.010(4)', level='Misdemeanor Class A', disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_misdemeanor_dismissal_is_eligible(self):
        charge = ChargeFactory.create(statute='813.010(4)', level='Misdemeanor Class A', disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(1)(b)'

    def test_felony_conviction_is_not_eligible(self):
        charge = ChargeFactory.create(statute='819.300', level='Felony Class C', disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_felony_dismissal_is_eligible(self):
        charge = ChargeFactory.create(statute='819.300', level='Felony Class C', disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(1)(b)'


class TestLevel800ViolationsInfractionsAreNotTypeEligible(unittest.TestCase):

    def setUp(self):
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.convicted = ['Convicted', last_week]
        self.dismissed= ['Dismissed', last_week]

    def test_convicted_violation_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute='801.000', level='Class C Traffic Violation', disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_dismissed_violation_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute='801.000', level='Class C Traffic Violation', disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_convicted_infraction_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute='811135', level='Infraction Class B', disposition=self.convicted)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_dismissed_infraction_is_not_type_eligible(self):
        charge = ChargeFactory.create(statute='811135', level='Infraction Class B', disposition=self.dismissed)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'


class TestViolationsInfractionsSkipAnalysis(unittest.TestCase):

    def setUp(self):
        self.convicted = ['Convicted', '05/05/2018']

    def test_violation_level_charge_skips_analysis(self):
        charge = ChargeFactory.create(statute='801.000', level='Class C Traffic Violation', disposition=self.convicted)

        assert charge.skip_analysis() is True

    def test_level_800_infractions_skip_analysis(self):
        charge = ChargeFactory.create(statute='811135', level='Infraction Class B', disposition=self.convicted)

        assert charge.skip_analysis() is True


class TestMisdemeanorFeloniesDoNotSkipAnalysis(unittest.TestCase):

    def setUp(self):
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.convicted = ['Convicted', last_week]
        self.dismissed= ['Dismissed', last_week]

    def test_misdemeanor_dismissal_does_not_skip_analysis(self):
        charge = ChargeFactory.create(statute='813.010(4)', level='Misdemeanor Class A', disposition=self.dismissed)

        assert charge.skip_analysis() is False

    def test_misdemeanor_conviction_does_not_skip_analysis(self):
        charge = ChargeFactory.create(statute='813.010(4)', level='Misdemeanor Class A', disposition=self.convicted)

        assert charge.skip_analysis() is False

    def test_felony_dismissal_does_not_skip_analysis(self):
        charge = ChargeFactory.create(statute='819.300', level='Felony Class C', disposition=self.dismissed)

        assert charge.skip_analysis() is False

    def test_felony_conviction_does_not_skip_analysis(self):
        charge = ChargeFactory.create(statute='819.300', level='Felony Class C', disposition=self.convicted)

        assert charge.skip_analysis() is False
