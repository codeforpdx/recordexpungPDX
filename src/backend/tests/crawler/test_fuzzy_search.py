import unittest

from expungeservice.crawler.fuzzy_search import FuzzySearch
from expungeservice.crawler.parsers.case_parser.case_parser import \
    PROBATION_REVOKED_SEARCH_TERMS

from tests.fixtures.case_details import CaseDetails

class TestFuzzySearch(unittest.TestCase):

    def test_simple_searches(self):
        text = "The quick brown fox jumps over the lazy dog."
        assert FuzzySearch.search(text, ["fox"])
        assert FuzzySearch.search(text, ["ffox"])
        assert FuzzySearch.search(text, ["FFOX"])
        assert not FuzzySearch.search(text, ["panda"])

    def test_simple_probation_revoked_search(self):
        text = """
        Comment: PROB REVOKED;
                Court Action: Signed; Court Action Date: 11/08/2010;
                Judge: Judge;
        """
        assert FuzzySearch.search(text, PROBATION_REVOKED_SEARCH_TERMS)

    def test_negative_probation_revoked_search(self):
        text = """
        Status: Superseded
                on: Apr 6 2010
                12:00AM
                Probation Cond.....
                All General
                Conditions Apply
                Sentence
                Status:Superseded
                Sentence
                Date:04/06/2010
                Guidelines: Severity
                1 History E
        """
        assert not FuzzySearch.search(text, PROBATION_REVOKED_SEARCH_TERMS)

    def test_simple_probation_revoked_search_with_html_tags(self):
        text = """
        ...
                           <td class="ssMenuText ssSmallText">
                        <div class="ssPreFormatted ssMenuText ssSmallText"
                             style="display:list-item;">
                             ...
                            Special Factor:
                            137.010 Presumptive
                            Sntc
                            PV Jail w/Credit
                            Time Srv 60 Day(s)
                            PV Post Prison Spvsn
                            1 Year(s)
                            PV Probation Revked
                        </div>
                    </td>
                </tr>
            </table>
        </nobr>
        """
        assert FuzzySearch.search(text, PROBATION_REVOKED_SEARCH_TERMS)

    def test_full_cases_for_revoked_probation(self):
        assert FuzzySearch.search(CaseDetails.CASE_WITH_REVOKED_PROBATION, PROBATION_REVOKED_SEARCH_TERMS)
        assert not FuzzySearch.search(CaseDetails.CASE_PARKING_VIOLATION, PROBATION_REVOKED_SEARCH_TERMS)
        assert not FuzzySearch.search(CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION, PROBATION_REVOKED_SEARCH_TERMS)