import unittest

from datetime import datetime, timedelta
from expungeservice.expungement_analyzer.type_analyzer import TypeAnalyzer
from expungeservice.crawler.models.charge import Charge
from expungeservice.crawler.models.charge import Disposition


class TestSingleChargeConvictions(unittest.TestCase):

    def setUp(self):
        self.type_analyzer = TypeAnalyzer()
        one_month_ago = (datetime.today() - timedelta(days=30)).strftime('%m/%d/%Y')
        last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
        self.single_charge = {'name': '', 'statute': '', 'level': '', 'date': one_month_ago}
        disposition = {'ruling': 'Convicted', 'date': last_week}
        self.convicted_disposition = Disposition(**disposition)
        self.charges = []

    def create_recent_charge(self):
        charge = Charge(**self.single_charge)
        charge.disposition = self.convicted_disposition
        return charge

    def test_felony_class_a_charge(self):
        self.single_charge['name'] = 'Assault in the first degree'
        self.single_charge['statute'] = '163.185'
        self.single_charge['level'] = 'Felony Class A'
        felony_class_a_convicted = self.create_recent_charge()
        self.charges.append(felony_class_a_convicted)
        self.type_analyzer.evaluate(self.charges)

        assert felony_class_a_convicted.expungement_result.type_eligibility is False
        assert felony_class_a_convicted.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_misdemeanor_sex_crime(self):
        self.single_charge['name'] = 'Sexual Abuse in the Third Degree'
        self.single_charge['statute'] = '163.415'
        self.single_charge['level'] = 'Misdemeanor Class A'
        misdemeanor_class_a_convicted = self.create_recent_charge()
        self.charges.append(misdemeanor_class_a_convicted)
        self.type_analyzer.evaluate(self.charges)

        assert misdemeanor_class_a_convicted.expungement_result.type_eligibility is False
        assert misdemeanor_class_a_convicted.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_min_statute_range_for_crimes_against_persons(self):
        self.single_charge['statute'] = '163.305'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_max_statute_range_for_crimes_against_persons(self):
        self.single_charge['statute'] = '163.479'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_min_statute_range_for_other_crimes_against_persons(self):
        self.single_charge['statute'] = '163.670'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_max_statute_range_for_other_crimes_against_persons(self):
        self.single_charge['statute'] = '163.693'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_min_statute_range_for_promoting_prostitution(self):
        self.single_charge['statute'] = '167.008'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_max_statute_range_for_promoting_prostitution(self):
        self.single_charge['statute'] = '167.107'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_min_statute_range_for_obscenity_and_minors(self):
        self.single_charge['statute'] = '167.057'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_max_statute_range_for_obscenity_and_minors(self):
        self.single_charge['statute'] = '167.080'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_traffic_crime_801_000(self):
        self.single_charge['statute'] = '801.000'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_traffic_crime_825_999(self):
        self.single_charge['statute'] = '825.999'
        convicted_charge = self.create_recent_charge()
        self.charges.append(convicted_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_charge.expungement_result.type_eligibility is False
        assert convicted_charge.expungement_result.reason == 'Ineligible under 137.225(5)'

    def test_poss_of_cocaine(self):
        self.single_charge['name'] = 'Possession of Cocaine'
        self.single_charge['statute'] = '475.884'
        self.single_charge['level'] = 'Felony Class C'
        convicted_cocaine_charge = self.create_recent_charge()
        self.charges.append(convicted_cocaine_charge)
        self.type_analyzer.evaluate(self.charges)

        assert convicted_cocaine_charge.expungement_result.type_eligibility is True
        assert convicted_cocaine_charge.expungement_result.reason == 'Eligible under 137.225(5)(b)'

    def test_misdemeanor(self):
        self.single_charge['name'] = 'Criminal Trespass in the Second Degree'
        self.single_charge['statute'] = '164.245'
        self.single_charge['level'] = 'Misdemeanor Class C'
        misdemeanor_charge = self.create_recent_charge()
        self.charges.append(misdemeanor_charge)
        self.type_analyzer.evaluate(self.charges)

        assert misdemeanor_charge.expungement_result.type_eligibility is True
        assert misdemeanor_charge.expungement_result.reason == 'Eligible under 137.225(5)(b)'

    def test_rape_class_c_felony(self):
        self.single_charge['name'] = 'Rape in the Third Degree'
        self.single_charge['statute'] = '163.355'
        self.single_charge['level'] = 'Felony Class C'
        sex_crime_charge = self.create_recent_charge()
        self.charges.append(sex_crime_charge)
        self.type_analyzer.evaluate(self.charges)

        assert sex_crime_charge.expungement_result.type_eligibility is False
        assert sex_crime_charge.expungement_result.reason == 'Ineligible under 137.225(5)'
