import datetime
import copy

from expungeservice.expunger import *

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


def get_disp():
    date = datetime.date(1996, 1, 1)
    disp_type = DispositionType.CONVICTED
    return Disposition(disp_type, date)

def test_expunger_classes():
    disp = get_disp()
    statute = Statute(113, 45, 5, 'd')
    level = CrimeLevel('Felony', 'A')
    charges = [
        Charge('Charge1', statute, level,
               datetime.date(1995, 1, 1), disp),
        Charge('Charge2', statute, level,
               datetime.date(1995, 1, 1), disp)
    ]
    cases = [
        Case(charges, CaseState.OPEN, 100.50),
        Case(charges, CaseState.CLOSED, 100.50),
    ]
    client = Client('John Doe', datetime.date(1970, 1, 1), cases)
    assert(client.num_charges() == 4)
