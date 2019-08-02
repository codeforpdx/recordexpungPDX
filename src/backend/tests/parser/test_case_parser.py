import datetime
import unittest

from expungeservice.crawler.parsers.case_parser.case_parser import CaseParser
from tests.fixtures.case_details import CaseDetails


class TestCaseWithDisposition(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_X1)

    # Tests charge data is collected for each row and column in the charge table
    # and is appended to the charge_table_data list grouped by rows.
    def test_it_parses_all_charge_rows(self):
        assert len(self.parser.charge_table_data) == 15

    def test_ids_are_collected(self):
        assert self.parser.charge_table_data[0] == '1.\n            \xa0'
        assert self.parser.charge_table_data[5] == '2.\n            \xa0'
        assert self.parser.charge_table_data[10] == '3.\n            \xa0'

    def test_charge_names_are_collected(self):
        assert self.parser.charge_table_data[1] == 'Driving Uninsured'
        assert self.parser.charge_table_data[6] == 'Violation Driving While Suspended or Revoked'
        assert self.parser.charge_table_data[11] == 'Failure to Obey Traffic Control Device'

    def test_statutes_are_collected(self):
        assert self.parser.charge_table_data[2] == '806.010'
        assert self.parser.charge_table_data[7] == '811.175'
        assert self.parser.charge_table_data[12] == '811.265'

    def test_charge_levels_are_collected(self):
        assert self.parser.charge_table_data[3] == 'Violation Class B'
        assert self.parser.charge_table_data[8] == 'Violation Class A'
        assert self.parser.charge_table_data[13] == 'Violation Class C'

    def test_charge_dates_are_collected(self):
        assert self.parser.charge_table_data[4] == '03/12/2017'
        assert self.parser.charge_table_data[9] == '04/01/2016'
        assert self.parser.charge_table_data[14] == '05/22/2015'

    # Tests disposition data is collected from the events table
    def test_it_parses_every_row_of_the_events_table(self):
        assert len(self.parser.event_table_data) == 14

    def test_it_collects_the_disposition_row(self):
        assert self.parser.event_table_data[1][0] == '06/12/2017'
        assert self.parser.event_table_data[1][3] == 'Disposition'
        assert self.parser.event_table_data[1][4] == ' (Judicial Officer: Office, Judicial M)'
        assert self.parser.event_table_data[1][5] == '1.\xa0Driving Uninsured'
        assert self.parser.event_table_data[1][6] == 'Convicted - Failure to Appear'
        assert self.parser.event_table_data[1][7] == '2. Violation Driving While Suspended or Revoked'
        assert self.parser.event_table_data[1][8] == 'Dismissed'
        assert self.parser.event_table_data[1][9] == '3. Failure to Obey Traffic Control Device'
        assert self.parser.event_table_data[1][10] == 'Dismissed'
        assert self.parser.event_table_data[1][11] == '\n        Created: 06/12/2017 2:57 PM'

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


class TestCaseWithoutFinancialTable(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION)

    # Tests charge data is collected for each row and column in the charge table
    # and is appended to the charge_table_data list grouped by rows.
    def test_it_parses_all_charge_rows(self):
        assert len(self.parser.charge_table_data) == 5

    def test_ids_are_collected(self):
        assert self.parser.charge_table_data[0] == '1.\n            \xa0'

    def test_charge_names_are_collected(self):
        assert self.parser.charge_table_data[1] == 'Poss Controlled Sub 2'

    def test_statutes_are_collected(self):
        assert self.parser.charge_table_data[2] == '4759924B'

    def test_charge_levels_are_collected(self):
        assert self.parser.charge_table_data[3] == 'Felony Class C'

    def test_charge_dates_are_collected(self):
        assert self.parser.charge_table_data[4] == '04/12/1992'

    # Tests disposition data is collected from the events table
    def test_it_parses_every_row_of_the_events_table(self):
        assert len(self.parser.event_table_data) == 14

    def test_it_collects_the_disposition_row(self):
        assert self.parser.event_table_data[0][0] == '04/30/1992'
        assert self.parser.event_table_data[0][3] == 'Disposition'
        assert self.parser.event_table_data[0][4] == ' (Judicial Officer: Unassigned, Judge)'
        assert self.parser.event_table_data[0][5] == '1. Poss Controlled Sub 2'
        assert self.parser.event_table_data[0][6] == 'Dismissed'
        assert self.parser.event_table_data[0][7] == '\n        Created: 05/01/1992 12:00 AM'

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


class TestCaseWithPartialDisposition(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_WITH_PARTIAL_DISPOS)

    # Tests charge data is collected for each row and column in the charge table
    # and is appended to the charge_table_data list grouped by rows.
    def test_it_parses_all_charge_rows(self):
        assert len(self.parser.charge_table_data) == 20

    def test_ids_are_collected(self):
        assert self.parser.charge_table_data[0] == '1.\n            \xa0'
        assert self.parser.charge_table_data[5] == '2.\n            \xa0'
        assert self.parser.charge_table_data[10] == '3.\n            \xa0'
        assert self.parser.charge_table_data[15] == '999.\n            \xa0'

    def test_charge_names_are_collected(self):
        assert self.parser.charge_table_data[1] == 'Reckless Driving'
        assert self.parser.charge_table_data[6] == 'Resisting Arrest'
        assert self.parser.charge_table_data[11] == 'Interfering w/ Peace/Parole and Probation Officer'
        assert self.parser.charge_table_data[16] == 'Driving Under the Influence of Intoxicants'

    def test_statutes_are_collected(self):
        assert self.parser.charge_table_data[2] == '811.140'
        assert self.parser.charge_table_data[7] == '162.315'
        assert self.parser.charge_table_data[12] == '162.247'
        assert self.parser.charge_table_data[17] == '813.010(4)'

    def test_charge_levels_are_collected(self):
        assert self.parser.charge_table_data[3] == 'Misdemeanor Class A'
        assert self.parser.charge_table_data[8] == 'Misdemeanor Class A'
        assert self.parser.charge_table_data[13] == 'Misdemeanor Class A'
        assert self.parser.charge_table_data[18] == 'Misdemeanor Class A'

    def test_charge_dates_are_collected(self):
        assert self.parser.charge_table_data[4] == '03/06/2018'
        assert self.parser.charge_table_data[9] == '03/06/2018'
        assert self.parser.charge_table_data[14] == '03/06/2018'
        assert self.parser.charge_table_data[19] == '03/06/2018'

    # Tests disposition data is collected from the events table
    def test_it_parses_every_row_of_the_events_table(self):
        assert len(self.parser.event_table_data) == 20

    def test_it_collects_the_disposition_row(self):
        assert self.parser.event_table_data[0][0] == '03/06/2018'
        assert self.parser.event_table_data[0][3] == 'Disposition'
        assert self.parser.event_table_data[0][4] == '999.\xa0Driving Under the Influence of Intoxicants'
        assert self.parser.event_table_data[0][5] == 'No Complaint'
        assert self.parser.event_table_data[0][6] == '\n        Created: 03/06/2018 1:07 PM'

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


class TestCaseWithoutDisposition(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_WITHOUT_DISPOS)

    # Tests charge data is collected for each row and column in the charge table
    # and is appended to the charge_table_data list grouped by rows.
    def test_it_parses_all_charge_rows(self):
        assert len(self.parser.charge_table_data) == 15

    def test_ids_are_collected(self):
        assert self.parser.charge_table_data[0] == '1.\n            \xa0'
        assert self.parser.charge_table_data[5] == '2.\n            \xa0'
        assert self.parser.charge_table_data[10] == '3.\n            \xa0'

    def test_charge_names_are_collected(self):
        assert self.parser.charge_table_data[1] == 'Reckless Driving'
        assert self.parser.charge_table_data[6] == 'Resisting Arrest'
        assert self.parser.charge_table_data[11] == 'Interfering w/ Peace/Parole and Probation Officer'

    def test_statutes_are_collected(self):
        assert self.parser.charge_table_data[2] == '811.140'
        assert self.parser.charge_table_data[7] == '162.315'
        assert self.parser.charge_table_data[12] == '162.247'

    def test_charge_levels_are_collected(self):
        assert self.parser.charge_table_data[3] == 'Misdemeanor Class A'
        assert self.parser.charge_table_data[8] == 'Misdemeanor Class A'
        assert self.parser.charge_table_data[13] == 'Misdemeanor Class A'

    def test_charge_dates_are_collected(self):
        assert self.parser.charge_table_data[4] == '03/06/2018'
        assert self.parser.charge_table_data[9] == '03/06/2018'
        assert self.parser.charge_table_data[14] == '03/06/2018'

    # Tests disposition data is collected from the events table
    def test_it_parses_every_row_of_the_events_table(self):
        assert len(self.parser.event_table_data) == 19

    def test_it_collects_the_disposition_row(self):
        dispo_count = 0
        for data in self.parser.event_table_data:
            if len(data) > 3 and data[3] == 'Disposition':
                dispo_count += 1
        assert dispo_count == 0

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


class TestParkingViolationCase(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_PARKING_VIOLATION)

    # Tests charge data is collected for each row and column in the charge table
    # and is appended to the charge_table_data list grouped by rows.
    def test_it_parses_all_charge_rows(self):
        assert len(self.parser.charge_table_data) == 5

    def test_ids_are_collected(self):
        assert self.parser.charge_table_data[0] == '1.\n            \xa0'

    def test_charge_names_are_collected(self):
        assert self.parser.charge_table_data[1] == 'No Meter Receipt'

    def test_statutes_are_collected(self):
        assert self.parser.charge_table_data[2] == '16.20.430-A'

    def test_charge_levels_are_collected(self):
        assert self.parser.charge_table_data[3] == 'Violation Unclassified'

    def test_charge_dates_are_collected(self):
        assert self.parser.charge_table_data[4] == '12/01/2018'

    # Tests disposition data is collected from the events table
    def test_it_parses_every_row_of_the_events_table(self):
        assert len(self.parser.event_table_data) == 1

    def test_it_collects_the_disposition_row(self):
        dispo_count = 0
        for data in self.parser.event_table_data:
            if len(data) > 3 and data[3] == 'Disposition':
                dispo_count += 1
        assert dispo_count == 0

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


class TestCaseWithRelatedCases(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASEJD74)

    def test_ids_are_collected(self):
        assert self.parser.charge_table_data[0] == '1.\n            \xa0'

    def test_charge_names_are_collected(self):
        assert self.parser.charge_table_data[1] == 'Poss Controlled Sub 2'

    def test_statutes_are_collected(self):
        assert self.parser.charge_table_data[2] == '4759924B'

    def test_charge_levels_are_collected(self):
        assert self.parser.charge_table_data[3] == 'Felony Class C'

    def test_charge_dates_are_collected(self):
        assert self.parser.charge_table_data[4] == '03/19/2000'

    # Tests disposition data is collected from the events table
    def test_it_parses_every_row_of_the_events_table(self):
        assert len(self.parser.event_table_data) == 14

    def test_it_collects_the_disposition_row(self):
        dispo_count = 0
        for data in self.parser.event_table_data:
            if len(data) > 3 and data[3] == 'Disposition':
                dispo_count += 1
        assert dispo_count == 1

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


class TestFelicia(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.COMMENTS_ENTERED_UNDER_SEPARATE_DISPOSITION_HEADERS)

    def test_ids_are_collected(self):
        assert self.parser.charge_table_data[0] == '1.\n            \xa0'
        assert self.parser.charge_table_data[5] == '2.\n            \xa0'

    def test_charge_names_are_collected(self):
        assert self.parser.charge_table_data[1] == 'Unauthorized Use of a Vehicle'
        assert self.parser.charge_table_data[6] == 'Possession of a Stolen Vehicle'

    def test_statutes_are_collected(self):
        assert self.parser.charge_table_data[2] == '164.135'
        assert self.parser.charge_table_data[7] == '819.300'

    def test_charge_levels_are_collected(self):
        assert self.parser.charge_table_data[3] == 'Felony Class C'
        assert self.parser.charge_table_data[8] == 'Felony Class C'

    def test_charge_dates_are_collected(self):
        assert self.parser.charge_table_data[4] == '05/13/2005'
        assert self.parser.charge_table_data[9] == '05/13/2005'

    def test_financial_data_is_parsed(self):
        assert self.parser.balance_due == '0.00'

    # Test data is formatted
    def test_dispo_data_gets_formatted(self):
        assert len(self.parser.hashed_dispo_data) == 2

        assert self.parser.hashed_dispo_data[1]['ruling'] == 'Convicted'
        assert self.parser.hashed_dispo_data[1]['date'] == '09/19/2005'

        assert self.parser.hashed_dispo_data[2]['ruling'] == 'Dismissed'
        assert self.parser.hashed_dispo_data[2]['date'] == '07/19/2005'
