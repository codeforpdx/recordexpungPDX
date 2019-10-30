import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestSingleChargeConvictions(unittest.TestCase):

    def setUp(self):
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling='Convicted', date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a_convicted = self.create_recent_charge()
        self.charges.append(felony_class_a_convicted)

        assert felony_class_a_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert felony_class_a_convicted.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_misdemeanor_sex_crime(self):
        self.single_charge['name'] = 'Sexual Abuse in the Third Degree'
        self.single_charge['statute'] = '163.415'
        self.single_charge['level'] = 'Misdemeanor Class A'
        misdemeanor_class_a_convicted = self.create_recent_charge()
        self.charges.append(misdemeanor_class_a_convicted)

        assert misdemeanor_class_a_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert misdemeanor_class_a_convicted.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_min_statute_range_for_crimes_against_persons(self):
        self.single_charge['statute'] = '163.305'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)

        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_max_statute_range_for_crimes_against_persons(self):
        self.single_charge['statute'] = '163.479'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)

        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_min_statute_range_for_other_crimes_against_persons(self):
        self.single_charge['statute'] = '163.670'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)

        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_max_statute_range_for_other_crimes_against_persons(self):
        self.single_charge['statute'] = '163.693'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)

        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_min_statute_range_for_promoting_prostitution(self):
        self.single_charge['statute'] = '167.008'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)

        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_max_statute_range_for_promoting_prostitution(self):
        self.single_charge['statute'] = '167.107'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)

        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_min_statute_range_for_obscenity_and_minors(self):
        self.single_charge['statute'] = '167.057'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)

        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_max_statute_range_for_obscenity_and_minors(self):
        self.single_charge['statute'] = '167.080'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)

        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_misdemeanor(self):
        self.single_charge['name'] = 'Criminal Trespass in the Second Degree'
        self.single_charge['statute'] = '164.245'
        self.single_charge['level'] = 'Misdemeanor Class C'
        misdemeanor_charge = self.create_recent_charge()
        self.charges.append(misdemeanor_charge)

        assert misdemeanor_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert misdemeanor_charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(b)'

    def test_rape_class_c_felony(self):
        self.single_charge['name'] = 'Rape in the Third Degree'
        self.single_charge['statute'] = '163.355'
        self.single_charge['level'] = 'Felony Class C'
        sex_crime_charge = self.create_recent_charge()
        self.charges.append(sex_crime_charge)

        assert sex_crime_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert sex_crime_charge.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_marijuana_ineligible_statute_475b3493c(self):
        self.single_charge['name'] = 'Unlawful Manufacture of Marijuana Item'
        self.single_charge['statute'] = '475B.349(3)(C)'
        self.single_charge['level'] = 'Felony Class C'
        marijuana_felony_class_c = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_c)

        assert marijuana_felony_class_c.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_c.expungement_result.type_eligibility.reason == 'Ineligible under 137.226'

    def test_marijuana_ineligible_statute_475b359(self):
        self.single_charge['name'] = 'Arson incident to manufacture of cannabinoid extract in first degree'
        self.single_charge['statute'] = '475b.359'
        self.single_charge['level'] = 'Felony Class A'
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == 'Ineligible under 137.226'

    def test_marijuana_ineligible_statute_475b367(self):
        self.single_charge['name'] = 'Causing another person to ingest marijuana'
        self.single_charge['statute'] = '475B.367'
        self.single_charge['level'] = 'Felony Class A'
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == 'Ineligible under 137.226'

    def test_marijuana_ineligible_statute_475b371(self):
        self.single_charge['name'] = 'Administration to another person under 18 years of age'
        self.single_charge['statute'] = '475B.371'
        self.single_charge['level'] = 'Felony Class A'
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == 'Ineligible under 137.226'

    def test_marijuana_ineligible_statute_167262(self):
        self.single_charge['name'] = 'Use of minor in controlled substance or marijuana item offense'
        self.single_charge['statute'] = '167.262'
        self.single_charge['level'] = 'Misdemeanor Class A'
        marijuana_misdemeanor_class_a = self.create_recent_charge()
        self.charges.append(marijuana_misdemeanor_class_a)

        assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_misdemeanor_class_a.expungement_result.type_eligibility.reason == 'Ineligible under 137.226'

    # List B Tests - Currently being marked as "Further Analysis Needed"

    def test_list_b_163200(self):
        self.single_charge['name'] = 'Criminal mistreatment in the second degree'
        self.single_charge['statute'] = '163.200'
        self.single_charge['level'] = 'Misdemeanor Class A'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_163205(self):
        self.single_charge['name'] = 'Criminal mistreatment in the first degree'
        self.single_charge['statute'] = '163.205'
        self.single_charge['level'] = 'Felony Class C'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_163575(self):
        self.single_charge['name'] = 'Endangering the welfare of a minor'
        self.single_charge['statute'] = '163.575'
        self.single_charge['level'] = 'Misdemeanor Class A'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_163535(self):
        self.single_charge['name'] = 'Abandonment of a child'
        self.single_charge['statute'] = '163.535'
        self.single_charge['level'] = 'Felony Class C'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_163175(self):
        self.single_charge['name'] = 'Assault in the second degree'
        self.single_charge['statute'] = '163.175'
        self.single_charge['level'] = 'Felony Class B'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_163275(self):
        self.single_charge['name'] = 'Coercion'
        self.single_charge['statute'] = '163.275'
        self.single_charge['level'] = 'Felony Class C'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_162165(self):
        self.single_charge['name'] = 'Escape in the first degree'
        self.single_charge['statute'] = '162.165'
        self.single_charge['level'] = 'Felony Class B'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_163525(self):
        self.single_charge['name'] = 'Incest'
        self.single_charge['statute'] = '163.525'
        self.single_charge['level'] = 'Felony Class C'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_164405(self):
        self.single_charge['name'] = 'Robbery in the second degree'
        self.single_charge['statute'] = '164.405'
        self.single_charge['level'] = 'Felony Class B'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_164395(self):
        self.single_charge['name'] = 'Robbery in the third degree'
        self.single_charge['statute'] = '164.395'
        self.single_charge['level'] = 'Felony Class C'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_162185(self):
        self.single_charge['name'] = 'Supplying contraband'
        self.single_charge['statute'] = '162.185'
        self.single_charge['level'] = 'Felony Class C'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_163225(self):
        self.single_charge['name'] = 'Kidnapping in the second degree'
        self.single_charge['statute'] = '163.225'
        self.single_charge['level'] = 'Felony Class B'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_163165(self):
        self.single_charge['name'] = 'Assault in the third degree'
        self.single_charge['statute'] = '163.165'
        self.single_charge['level'] = 'Felony Class C'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_list_b_166220(self):
        self.single_charge['name'] = 'Unlawful use of weapon'
        self.single_charge['statute'] = '166.220'
        self.single_charge['level'] = 'Felony Class C'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    # Test sub-chapters are not compared when not necessary.

    def test_list_b_charge_that_includes_sub_chapter(self):
        self.single_charge['name'] = 'Unlawful use of weapon'
        self.single_charge['statute'] = '166.220(1)(b)'
        self.single_charge['level'] = 'Felony Class C'
        list_b_charge = self.create_recent_charge()
        self.charges.append(list_b_charge)

        assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert list_b_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_marijuana_ineligible_statute_475b3592a(self):
        self.single_charge['name'] = 'Arson incident to manufacture of cannabinoid extract in first degree'
        self.single_charge['statute'] = '475b.359(2)(a)'
        self.single_charge['level'] = 'Felony Class A'
        marijuana_felony_class_a = self.create_recent_charge()
        self.charges.append(marijuana_felony_class_a)

        assert marijuana_felony_class_a.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert marijuana_felony_class_a.expungement_result.type_eligibility.reason == 'Ineligible under 137.226'

    # Possession of controlled substance tests

    def test_pcs_475854(self):
        self.single_charge['name'] = 'Unlawful possession of heroin'
        self.single_charge['statute'] = '475.854'
        self.single_charge['level'] = 'Misdemeanor Class A'
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(C)'

    def test_pcs_475874(self):
        self.single_charge['name'] = 'Unlawful possession of 3,4-methylenedioxymethamphetamine'
        self.single_charge['statute'] = '475.874'
        self.single_charge['level'] = 'Misdemeanor Class A'
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(C)'

    def test_pcs_475884(self):
        self.single_charge['name'] = 'Unlawful possession of cocaine'
        self.single_charge['statute'] = '475.884'
        self.single_charge['level'] = 'Misdemeanor Class A'
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(C)'

    def test_pcs_475894(self):
        self.single_charge['name'] = 'Unlawful possession of methamphetamine'
        self.single_charge['statute'] = '475.894'
        self.single_charge['level'] = 'Misdemeanor Class A'
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(C)'

    # Eligible misdemeanor and class C felony tests

    def test_misdemeanor_164043(self):
        self.single_charge['name'] = 'Theft in the third degree'
        self.single_charge['statute'] = '164.043'
        self.single_charge['level'] = 'Misdemeanor Class C'
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(b)'

    def test_misdemeanor_164055(self):
        self.single_charge['name'] = 'Theft in the first degree'
        self.single_charge['statute'] = '164.055'
        self.single_charge['level'] = 'Felony Class C'
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(b)'

    def test_misdemeanor_164125(self):
        self.single_charge['name'] = 'Theft of services'
        self.single_charge['statute'] = '164.125'
        self.single_charge['level'] = 'Misdemeanor Class A'
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(b)'

    def test_drug_free_zone_variance_misdemeanor(self):
        self.single_charge['name'] = '	Drug Free Zone Variance'
        self.single_charge['statute'] = '14B20060'
        self.single_charge['level'] = 'Misdemeanor Unclassified'
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(b)'

    def test_class_b_felony_164057(self):
        self.single_charge['name'] = 'Aggravated theft in the first degree'
        self.single_charge['statute'] = '164.057'
        self.single_charge['level'] = 'Felony Class B'
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

    def test_class_felony_is_added_to_b_felony_attribute(self):
        self.single_charge['name'] = 'Aggravated theft in the first degree'
        self.single_charge['statute'] = '164.057'
        self.single_charge['level'] = 'Felony Class B'
        charge = self.create_recent_charge()

        assert charge.__class__.__name__ == 'FelonyClassB'

    def test_charge_that_falls_through(self):
        self.single_charge['name'] = 'Aggravated theft in the first degree'
        self.single_charge['statute'] = '164.057'
        self.single_charge['level'] = 'Felony Class F'
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert charge.expungement_result.type_eligibility.reason == 'Examine'

    # Test non-traffic violation

    def test_non_traffic_violation(self):
        self.single_charge['name'] = 'Viol Treatment'
        self.single_charge['statute'] = '1615662'
        self.single_charge['level'] = 'Violation Unclassified'
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(d)'


class TestMultipleCharges(unittest.TestCase):

    def setUp(self):
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        disposition = Disposition(ruling='Convicted', date=last_week)
        self.charge = ChargeFactory.build(disposition=disposition)
        self.charges = []

    def create_charge(self):
        charge = ChargeFactory.save(self.charge)
        return charge

    def test_two_charges(self):
        # first charge
        self.charge['name'] = 'Theft of services'
        self.charge['statute'] = '164.125'
        self.charge['level'] = 'Misdemeanor Class A'
        charge = self.create_charge()
        self.charges.append(charge)

        # second charge
        self.charge['name'] = 'Traffic Violation'
        self.charge['statute'] = '801.000'
        self.charge['level'] = 'Class C Traffic Violation'
        charge = self.create_charge()
        self.charges.append(charge)

        assert self.charges[0].expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert self.charges[0].expungement_result.type_eligibility.reason == 'Eligible under 137.225(5)(b)'

        assert self.charges[1].expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert self.charges[1].expungement_result.type_eligibility.reason == 'Ineligible under 137.225(5)'

    def test_multiple_class_b_felonies_are_added_to_b_felony_list(self):
        # first charge
        self.charge['name'] = 'Theft of services'
        self.charge['statute'] = '164.125'
        self.charge['level'] = 'Misdemeanor Class A'
        charge = self.create_charge()
        self.charges.append(charge)

        # B felony
        self.charge['name'] = 'Aggravated theft in the first degree'
        self.charge['statute'] = '164.057'
        self.charge['level'] = 'Felony Class B'
        charge_1 = self.create_charge()
        self.charges.append(charge_1)

        # Second B felony
        self.charge['name'] = 'Aggravated theft in the first degree'
        self.charge['statute'] = '164.057'
        self.charge['level'] = 'Felony Class B'
        charge_2 = self.create_charge()
        self.charges.append(charge_2)

        assert charge_1.__class__.__name__ == 'FelonyClassB'
        assert charge_2.__class__.__name__ == 'FelonyClassB'
