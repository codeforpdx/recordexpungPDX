import unittest

from expungeservice.models.case import CaseCreator
from tests.factories.case_factory import CaseSummaryFactory


class TestCaseBalanceDue(unittest.TestCase):
    def test_balance_due_getter_setter(self):
        case_args = [("John Doe", "1990"), "", "", "", "", ("1/1/2019", ""), ("", ""), "", False]

        case_1 = CaseCreator.create(*case_args, "123.45")  # type: ignore
        assert case_1.get_balance_due() == 123.45

        case_2 = CaseCreator.create(*case_args, "2,345.67")  # type: ignore
        assert case_2.get_balance_due() == 2345.67

        case_3 = CaseCreator.create(*case_args, "0")  # type: ignore
        assert case_3.get_balance_due() == 0


class TestCaseClosedMethod(unittest.TestCase):
    def test_it_returns_true_for_a_closed_case(self):
        case = CaseSummaryFactory.create(type_status=["Offense Misdemeanor", "Closed"])
        assert case.closed() is True

    def test_it_returns_false_for_an_open_case(self):
        case = CaseSummaryFactory.create(type_status=["Offense Misdemeanor", "Open"])
        assert case.closed() is False

    def test_it_returns_true_for_an_inactive_case(self):
        case = CaseSummaryFactory.create(type_status=["Offense Misdemeanor", "Inactive"])
        assert case.closed() is True

    def test_it_returns_true_for_a_purged_case(self):
        case = CaseSummaryFactory.create(type_status=["Offense Misdemeanor", "Purgable"])
        assert case.closed() is True

    def test_it_returns_true_for_a_bankeruptcy_case(self):
        case = CaseSummaryFactory.create(type_status=["Offense Misdemeanor", "Bankruptcy Pending"])
        assert case.closed() is True


class TestBirthYearInitializesGivenMultipleValues(unittest.TestCase):
    def test_birth_year_defaults_to_empty_string(self):
        case = CaseSummaryFactory.create(info=["John Doe"])

        assert case.birth_year is None

    def test_it_assigns_birth_year_when_given_the_year(self):
        case = CaseSummaryFactory.create(info=["John Doe", "1979"])

        assert case.birth_year == 1979

    def test_it_assigns_birth_year_when_given_the_month_day_year_format(self):
        case = CaseSummaryFactory.create(info=["John Doe", "12/21/1979"])

        assert case.birth_year == 1979
