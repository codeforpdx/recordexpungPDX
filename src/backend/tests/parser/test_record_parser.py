import unittest
import datetime

from ..fixtures.john_doe import JohnDoe
from expungeservice.crawler.parsers.record_parser import RecordParser


class TestRecordParser(unittest.TestCase):

    def setUp(self):
        self.parser = RecordParser()
        self.parser.feed(JohnDoe.RECORD)
        self.case1_date = datetime.date(1963, 3, 23)
        self.case2_date = datetime.date(1963, 4, 11)
        self.case3_date = datetime.date(2012, 4, 1)
        self.base_uri = "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID="

    def test_non_empty_record(self):
        """Tests it can parse a record."""
        assert len(self.parser.cases) == 3

    def test_it_assigns_case_info(self):
        for case in self.parser.cases:
            assert case.name == "Doe, John D"
            assert case.birth_year == 1943

    def test_it_assigns_case_number(self):
        assert self.parser.cases[0].case_number == "X0001"
        assert self.parser.cases[1].case_number == "X0002"
        assert self.parser.cases[2].case_number == "X0003"

    def test_it_assigns_link_to_case(self):
        assert self.parser.cases[0].case_detail_link == self.base_uri + "X0001"
        assert self.parser.cases[1].case_detail_link == self.base_uri + "X0002"
        assert self.parser.cases[2].case_detail_link == self.base_uri + "X0003"

    def test_it_assigns_citation(self):
        assert self.parser.cases[0].citation_number == "C0001"
        assert self.parser.cases[1].citation_number == "C0002"
        assert self.parser.cases[2].citation_number == ""

    def test_it_assigns_date_location(self):
        assert self.parser.cases[0].date == self.case1_date
        assert self.parser.cases[0].location == "Multnomah"

        assert self.parser.cases[1].date == self.case2_date
        assert self.parser.cases[1].location == "Multnomah"

        assert self.parser.cases[2].date == self.case3_date
        assert self.parser.cases[2].location == "Multnomah"

    def test_it_assigns_violation_status_info(self):
        assert self.parser.cases[0].violation_type == "Offense Misdemeanor"
        assert self.parser.cases[0].current_status == "Closed"

        assert self.parser.cases[1].violation_type == "Offense Felony"
        assert self.parser.cases[1].current_status == "Closed"

        assert self.parser.cases[2].violation_type == "Offense Misdemeanor"
        assert self.parser.cases[2].current_status == "Open"

    def test_it_assigns_charges(self):
        assert len(self.parser.cases[0].charges) == 0
        assert len(self.parser.cases[1].charges) == 0
        assert len(self.parser.cases[2].charges) == 0


class TestEmptyRecord(unittest.TestCase):

    def test_empty_record(self):
        """Tests it can parse a blank record."""
        parser = RecordParser()
        parser.feed(JohnDoe.BLANK_RECORD)

        assert len(parser.cases) == 0


class TestRecordWithoutBirthYear(unittest.TestCase):

    def test_it_assigns_birth_year(self):
        parser = RecordParser()
        parser.feed(JohnDoe.RECORD_WITH_MISSING_BIRTH_YEAR)

        assert parser.cases[0].birth_year == 1943
        assert parser.cases[1].birth_year == 1943
        assert parser.cases[2].birth_year == ''
