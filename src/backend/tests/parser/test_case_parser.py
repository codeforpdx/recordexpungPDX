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
