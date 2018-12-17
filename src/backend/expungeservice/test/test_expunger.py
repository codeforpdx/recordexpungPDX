import datetime

from expungeservice.expunger import *

def test_statute():
    tests = [
        [[113, 45], '113.045'],
        [[113, 45, 5], '113.045 5'],
        [[113, 45, 5, 'd'], '113.045 5(d)'],
    ]
    for t in tests:
        if len(t[0]) == 4:
            assert(str(Statute(t[0][0], t[0][1], t[0][2], t[0][3])) == t[1])
        elif len(t[0]) == 3:
            assert(str(Statute(t[0][0], t[0][1], t[0][2])) == t[1])
        elif len(t[0]) == 2:
            assert(str(Statute(t[0][0], t[0][1])) == t[1])
        else:
            assert(0)

def get_disp():
    date = datetime.date(1996, 1, 1)
    disp_type = DispositionType.NO_CONVICTION
    return Disposition(disp_type, date)

def test_expunger_classes():
    disp = get_disp()
    statute = Statute(113, 45, 5, 'd')
    level = Level('Felony', 'A')
    charges = [
        Charge('Charge Name', statute, level,
               datetime.date(1995, 1, 1), disp)
    ]
    cases = [Case(charges, CaseState.OPEN), 100.50]
    client = Client('John Doe', datetime.date(1970, 1, 1), cases)
