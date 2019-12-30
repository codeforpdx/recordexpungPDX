import unittest

from expungeservice.crawler.parsers.case_parser import CaseParser
from tests.fixtures.case_details import CaseDetails


class TestCaseWithDisposition(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_X1)

    # Test relevant financial data is collected
    def test_financial_data_is_parsed(self):
        assert self.parser.balance_due == '1,516.80'

    # Test data is formatted
    def test_dispo_data_gets_formatted(self):
        assert len(self.parser.hashed_dispo_data) == 3
        assert self.parser.hashed_dispo_data[1]['date'] == '06/12/2017'
        assert self.parser.hashed_dispo_data[1]['charge'] == 'Driving Uninsured'
        assert self.parser.hashed_dispo_data[1]['ruling'] == 'Convicted - Failure to Appear'

        assert self.parser.hashed_dispo_data[2]['date'] == '06/12/2017'
        assert self.parser.hashed_dispo_data[2]['charge'] == 'Violation Driving While Suspended or Revoked'
        assert self.parser.hashed_dispo_data[2]['ruling'] == 'Dismissed'

        assert self.parser.hashed_dispo_data[3]['date'] == '06/12/2017'
        assert self.parser.hashed_dispo_data[3]['charge'] == 'Failure to Obey Traffic Control Device'
        assert self.parser.hashed_dispo_data[3]['ruling'] == 'Dismissed'

    def test_charge_data_is_formatted(self):
        assert len(self.parser.hashed_charge_data) == 3

        assert self.parser.hashed_charge_data[1]['name'] == 'Driving Uninsured'
        assert self.parser.hashed_charge_data[2]['name'] == 'Violation Driving While Suspended or Revoked'
        assert self.parser.hashed_charge_data[3]['name'] == 'Failure to Obey Traffic Control Device'

        assert self.parser.hashed_charge_data[1]['statute'] == '806.010'
        assert self.parser.hashed_charge_data[2]['statute'] == '811.175'
        assert self.parser.hashed_charge_data[3]['statute'] == '811.265'

        assert self.parser.hashed_charge_data[1]['level'] == 'Violation Class B'
        assert self.parser.hashed_charge_data[2]['level'] == 'Violation Class A'
        assert self.parser.hashed_charge_data[3]['level'] == 'Violation Class C'

        assert self.parser.hashed_charge_data[1]['date'] == '03/12/2017'
        assert self.parser.hashed_charge_data[2]['date'] == '04/01/2016'
        assert self.parser.hashed_charge_data[3]['date'] == '05/22/2015'

    def test_probation_revoked_is_parsed(self):
        assert not self.parser.probation_revoked


class TestCaseWithoutFinancialTable(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION)

    # Test relevant financial data is collected
    def test_financial_data_is_parsed(self):
        assert self.parser.balance_due == '0'

    # Test data is formatted
    def test_dispo_data_gets_formatted(self):
        assert len(self.parser.hashed_dispo_data) == 1
        assert self.parser.hashed_dispo_data[1]['date'] == '04/30/1992'
        assert self.parser.hashed_dispo_data[1]['charge'] == 'Poss Controlled Sub 2'
        assert self.parser.hashed_dispo_data[1]['ruling'] == 'Dismissed'

    def test_charge_data_is_formatted(self):
        assert len(self.parser.hashed_charge_data) == 1

        assert self.parser.hashed_charge_data[1]['name'] == 'Poss Controlled Sub 2'
        assert self.parser.hashed_charge_data[1]['statute'] == '4759924B'
        assert self.parser.hashed_charge_data[1]['level'] == 'Felony Class C'
        assert self.parser.hashed_charge_data[1]['date'] == '04/12/1992'

    def test_probation_revoked_is_parsed(self):
        assert not self.parser.probation_revoked


class TestCaseWithPartialDisposition(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_WITH_PARTIAL_DISPOS)

    # Test relevant financial data is collected
    def test_financial_data_is_parsed(self):
        assert self.parser.balance_due == '0'

    # Test data is formatted
    def test_dispo_data_gets_formatted(self):
        assert len(self.parser.hashed_dispo_data) == 1
        assert self.parser.hashed_dispo_data[999]['date'] == '03/06/2018'
        assert self.parser.hashed_dispo_data[999]['charge'] == 'Driving Under the Influence of Intoxicants'
        assert self.parser.hashed_dispo_data[999]['ruling'] == 'No Complaint'

    def test_charge_data_is_formatted(self):
        assert len(self.parser.hashed_charge_data) == 4

        assert self.parser.hashed_charge_data[1]['name'] == 'Reckless Driving'
        assert self.parser.hashed_charge_data[2]['name'] == 'Resisting Arrest'
        assert self.parser.hashed_charge_data[3]['name'] == 'Interfering w/ Peace/Parole and Probation Officer'
        assert self.parser.hashed_charge_data[999]['name'] == 'Driving Under the Influence of Intoxicants'

        assert self.parser.hashed_charge_data[1]['statute'] == '811.140'
        assert self.parser.hashed_charge_data[2]['statute'] == '162.315'
        assert self.parser.hashed_charge_data[3]['statute'] == '162.247'
        assert self.parser.hashed_charge_data[999]['statute'] == '813.010(4)'

        assert self.parser.hashed_charge_data[1]['level'] == 'Misdemeanor Class A'
        assert self.parser.hashed_charge_data[2]['level'] == 'Misdemeanor Class A'
        assert self.parser.hashed_charge_data[3]['level'] == 'Misdemeanor Class A'
        assert self.parser.hashed_charge_data[999]['level'] == 'Misdemeanor Class A'

        assert self.parser.hashed_charge_data[1]['date'] == '03/06/2018'
        assert self.parser.hashed_charge_data[2]['date'] == '03/06/2018'
        assert self.parser.hashed_charge_data[3]['date'] == '03/06/2018'
        assert self.parser.hashed_charge_data[999]['date'] == '03/06/2018'

    def test_probation_revoked_is_parsed(self):
        assert not self.parser.probation_revoked


class TestCaseWithoutDisposition(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_WITHOUT_DISPOS)

    # Test relevant financial data is collected
    def test_financial_data_is_parsed(self):
        assert self.parser.balance_due == '0'

    # Test data is formatted
    def test_dispo_data_gets_formatted(self):
        assert len(self.parser.hashed_dispo_data) == 0

    def test_charge_data_is_formatted(self):
        assert len(self.parser.hashed_charge_data) == 3

        assert self.parser.hashed_charge_data[1]['name'] == 'Reckless Driving'
        assert self.parser.hashed_charge_data[2]['name'] == 'Resisting Arrest'
        assert self.parser.hashed_charge_data[3]['name'] == 'Interfering w/ Peace/Parole and Probation Officer'

        assert self.parser.hashed_charge_data[1]['statute'] == '811.140'
        assert self.parser.hashed_charge_data[2]['statute'] == '162.315'
        assert self.parser.hashed_charge_data[3]['statute'] == '162.247'

        assert self.parser.hashed_charge_data[1]['level'] == 'Misdemeanor Class A'
        assert self.parser.hashed_charge_data[2]['level'] == 'Misdemeanor Class A'
        assert self.parser.hashed_charge_data[3]['level'] == 'Misdemeanor Class A'

        assert self.parser.hashed_charge_data[1]['date'] == '03/06/2018'
        assert self.parser.hashed_charge_data[2]['date'] == '03/06/2018'
        assert self.parser.hashed_charge_data[3]['date'] == '03/06/2018'

    def test_probation_revoked_is_parsed(self):
        assert not self.parser.probation_revoked


class TestParkingViolationCase(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_PARKING_VIOLATION)

    # Test relevant financial data is collected
    def test_financial_data_is_parsed(self):
        assert self.parser.balance_due == '65.00'

    # Test data is formatted
    def test_dispo_data_gets_formatted(self):
        assert len(self.parser.hashed_dispo_data) == 0

    def test_charge_data_is_formatted(self):
        assert len(self.parser.hashed_charge_data) == 1

        assert self.parser.hashed_charge_data[1]['name'] == 'No Meter Receipt'
        assert self.parser.hashed_charge_data[1]['statute'] == '16.20.430-A'
        assert self.parser.hashed_charge_data[1]['level'] == 'Violation Unclassified'
        assert self.parser.hashed_charge_data[1]['date'] == '12/01/2018'

    def test_probation_revoked_is_parsed(self):
        assert not self.parser.probation_revoked


class TestCaseWithRelatedCases(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASEJD74)

    # Test relevant financial data is collected
    def test_financial_data_is_parsed(self):
        assert self.parser.balance_due == '535.70'

    # Test data is formatted
    def test_dispo_data_gets_formatted(self):
        assert len(self.parser.hashed_dispo_data) == 1

        assert self.parser.hashed_dispo_data[1]['ruling'] == 'Convicted'
        assert self.parser.hashed_dispo_data[1]['date'] == '05/10/2000'

    def test_charge_data_is_formatted(self):
        assert len(self.parser.hashed_charge_data) == 1

        assert self.parser.hashed_charge_data[1]['name'] == 'Poss Controlled Sub 2'
        assert self.parser.hashed_charge_data[1]['statute'] == '4759924B'
        assert self.parser.hashed_charge_data[1]['level'] == 'Felony Class C'
        assert self.parser.hashed_charge_data[1]['date'] == '03/19/2000'

    def test_probation_revoked_is_parsed(self):
        assert not self.parser.probation_revoked


class TestFelicia(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.COMMENTS_ENTERED_UNDER_SEPARATE_DISPOSITION_HEADERS)

    def test_financial_data_is_parsed(self):
        assert self.parser.balance_due == '0.00'

    # Test data is formatted
    def test_dispo_data_gets_formatted(self):
        assert len(self.parser.hashed_dispo_data) == 2

        assert self.parser.hashed_dispo_data[1]['ruling'] == 'Convicted'
        assert self.parser.hashed_dispo_data[1]['date'] == '09/19/2005'

        assert self.parser.hashed_dispo_data[2]['ruling'] == 'Dismissed'
        assert self.parser.hashed_dispo_data[2]['date'] == '07/19/2005'

    def test_charge_data_is_formatted(self):
        assert len(self.parser.hashed_charge_data) == 2

        assert self.parser.hashed_charge_data[1]['name'] == 'Unauthorized Use of a Vehicle'
        assert self.parser.hashed_charge_data[1]['statute'] == '164.135'
        assert self.parser.hashed_charge_data[1]['level'] == 'Felony Class C'
        assert self.parser.hashed_charge_data[1]['date'] == '05/13/2005'

        assert self.parser.hashed_charge_data[2]['name'] == 'Possession of a Stolen Vehicle'
        assert self.parser.hashed_charge_data[2]['statute'] == '819.300'
        assert self.parser.hashed_charge_data[2]['level'] == 'Felony Class C'
        assert self.parser.hashed_charge_data[2]['date'] == '05/13/2005'

    def test_probation_revoked_is_parsed(self):
        assert not self.parser.probation_revoked


class TestRevokedProbation(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_WITH_REVOKED_PROBATION)

    def test_financial_data_is_parsed(self):
        assert self.parser.balance_due == '529.08'

    # Test data is formatted
    def test_dispo_data_gets_formatted(self):
        assert len(self.parser.hashed_dispo_data) == 2

        assert self.parser.hashed_dispo_data[1]['ruling'] == 'Convicted'
        assert self.parser.hashed_dispo_data[1]['date'] == '07/06/2009'

        assert self.parser.hashed_dispo_data[2]['ruling'] == 'Removed From Charging Instrument'
        assert self.parser.hashed_dispo_data[2]['date'] == '06/22/2009'

    def test_charge_data_is_formatted(self):
        assert len(self.parser.hashed_charge_data) == 2

        assert self.parser.hashed_charge_data[1]['name'] == 'Possession of Cocaine'
        assert self.parser.hashed_charge_data[1]['statute'] == '475.884'
        assert self.parser.hashed_charge_data[1]['level'] == 'Felony Class C'
        assert self.parser.hashed_charge_data[1]['date'] == '06/13/2009'

        assert self.parser.hashed_charge_data[2]['name'] == 'Possession of Cocaine'
        assert self.parser.hashed_charge_data[2]['statute'] == '475.884'
        assert self.parser.hashed_charge_data[2]['level'] == 'Felony Class C'
        assert self.parser.hashed_charge_data[2]['date'] == '02/17/2009'

    def test_probation_revoked_is_parsed(self):
        assert self.parser.probation_revoked


class TestSpacesExistingInChargeInfoCells(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CHARGE_INFO_WITH_EMPTY_DATA_CELLS)

    def test_it_parses_all_charge_rows(self):
        assert len(self.parser.hashed_charge_data) == 10
