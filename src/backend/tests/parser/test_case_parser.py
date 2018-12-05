import datetime
import unittest

from expungeservice.crawler.parsers.case_parser import CaseParser
from tests.fixtures.case_details import CaseDetails


class TestCaseWithDisposition(unittest.TestCase):

    def setUp(self):
        self.parser = CaseParser()
        self.parser.feed(CaseDetails.CASE_X1)

    def test_it_finds_the_start_of_each_table(self):
        assert self.parser.current_table_number == 4


class TestChargeTableIsParsed(TestCaseWithDisposition):
    """ Tests charge data is collected for each row and column in the charge table
        and appended to the charge_table_data list grouped by rows."""

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
