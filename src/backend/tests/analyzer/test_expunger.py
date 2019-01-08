
import copy
import unittest

from objbrowser import browse

from expungeservice.expunger.analyze import *
from expungeservice.expunger.client_builder import *
from expungeservice.models.disposition import DispositionType

import datetime

def test_statute():
    tests = [
        [[113, 45], '113.045'],
        [[113, 45, 5], '113.045(5)'],
        [[113, 45, 5, 'd'], '113.045(5)(d)'],
    ]
    for t in tests:
        if len(t[0]) == 4:
            s1 = Statute(t[0][0], t[0][1], t[0][2], t[0][3])
            s2 = copy.deepcopy(s1)
            assert(s1 == s2)
            assert(str(s1) == t[1])
        elif len(t[0]) == 3:
            s1 = Statute(t[0][0], t[0][1], t[0][2])
            s2 = copy.deepcopy(s1)
            assert(s1 == s2)
            assert(str(s1) == t[1])
        elif len(t[0]) == 2:
            s1 = Statute(t[0][0], t[0][1])
            s2 = copy.deepcopy(s1)
            assert(s1 == s2)
            assert(str(s1) == t[1])
        else:
            assert(0)

# get disposition helper function
def get_disp():
    date = datetime.date(1996, 1, 1)
    disp_type = DispositionType.NO_CONVICTION
    return Disposition(disp_type, date)

def get_convicted_disp():
    return Disposition(DispositionType.CONVICTED, datetime.date(1996, 1, 1))

def get_dummy_statute():
    return Statute(113, 45, 5, 'd')

def get_charge_crime_level(type_, class_):
    disp = get_convicted_disp()
    statute = get_dummy_statute()
    level = CrimeLevel(type_, class_)

    return Charge('%s %s charge' % (type_, class_), statute, level,
                  datetime.date(1995, 1, 1), disp)



"""
This mainly tests if we're able to construct the objects.
"""
def test_expunger_classes():

    charges = [
        get_charge_crime_level('Felony', 'A'),
        get_charge_crime_level('Felony', 'B')
    ]

    cases = [
        Case('doe, john', '01/01/1970', "case#1", "citation#1", "1/1/1111", "clack county", "felony", CaseState.OPEN, charges,
             "casedetail1.html", "OPEN", 100.50),
        Case('doe, john', '01/01/1970', "case#2", "citation#2", "2/2/2222", "clack county", "felony", CaseState.OPEN, charges,
             "casedetail1.html", "OPEN", 100.50)
    ]

    client = Client('John Doe', datetime.date(1970, 1, 1), cases)

    assert(client.num_charges() == 4)



class TestExpunger(unittest.TestCase):
    def setUp(self):
        test_expunger_classes()

        charges = [
            get_charge_crime_level('Felony', 'A'),
            get_charge_crime_level('Felony', 'B')
        ]

        self.open_case = Case('doe, john',
                              '01/01/1970',
                              "case#1",
                              "citation#1",
                              "1/1/1111",
                              "clack county",
                              "felony",
                              "open",
                              charges,
                              "casedetail1.html",
                              CaseState.OPEN, #casestate.open
                              5.50)

        self.closed_case = Case('doe, john',
                              '01/01/1970',
                              "case#1",
                              "citation#1",
                              "1/1/1111",
                              "clack county",
                              "felony",
                              "open",
                                charges,
                              "casedetail1.html",
                              CaseState.CLOSED,
                              100.50)

        # add case(s) when using this in a test
        self.client = Client('John Doe', datetime.date(1970, 1, 1), [self.open_case, self.closed_case])

        #print(self.client.toJSON())

        self.statute_137_225_5 = Statute(137, 225, 5)

    def test_type_elig_felony(self):

        record_analyzer = RecordAnalyzer(self.client)

        browse(record_analyzer)

        result = record_analyzer.type_eligibility(
                    get_charge_crime_level('Felony', 'A'))


        assert(result.code == ResultCode.INELIGIBLE)
        assert(result.statute == self.statute_137_225_5)

    def test_time_elig_open_case(self):

        self.client.cases = [self.closed_case, self.open_case]

        record_analyzer = RecordAnalyzer(self.client)

        result = record_analyzer.time_eligibility()
        assert(result.code == ResultCode.OPEN_CASE)



# if __name__ == '__main__':
#     test_expunger_classes()



