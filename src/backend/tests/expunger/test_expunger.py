import unittest

from expungeservice.expunger.expunger import Expunger
from expungeservice.models.disposition import Disposition
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.utilities.time import Time


class TestExpungementAnalyzerUnitTests(unittest.TestCase):

    def test_expunger_sets_most_recent_dismissal_when_charge_is_less_than_3yrs(self):
        case = CaseFactory.create()
        mrd_charge = ChargeFactory.create_dismissed_charge(date=Time.LESS_THAN_THREE_YEARS_AGO)
        case.charges = [mrd_charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_dismissal is mrd_charge

    def test_expunger_does_not_set_most_recent_dismissal_when_case_is_older_than_3yrs(self):
        case = CaseFactory.create()
        charge_1 = ChargeFactory.create_dismissed_charge(date=Time.THREE_YEARS_AGO)
        charge_2 = ChargeFactory.create_dismissed_charge(date=Time.THREE_YEARS_AGO)
        case.charges = [charge_1, charge_2]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_dismissal is None

    def test_expunger_sets_mrd_when_mrd_is_in_middle_of_list(self):
        case = CaseFactory.create()
        mrd_charge = ChargeFactory.create_dismissed_charge(date=Time.TWO_YEARS_AGO)
        charge = ChargeFactory.create_dismissed_charge(date=Time.LESS_THAN_THREE_YEARS_AGO)
        case.charges = [charge, charge, mrd_charge, charge, charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_dismissal is mrd_charge

    def test_expunger_sets_mrd_when_mrd_is_at_end_of_list(self):
        case = CaseFactory.create()
        mrd_charge = ChargeFactory.create_dismissed_charge(date=Time.TWO_YEARS_AGO)
        charge = ChargeFactory.create_dismissed_charge(date=Time.LESS_THAN_THREE_YEARS_AGO)
        case.charges = [charge, charge, mrd_charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_dismissal is mrd_charge

    def test_it_skips_closed_cases_without_dispositions(self):
        case = CaseFactory.create()
        charge_without_dispo = ChargeFactory.create()
        case.charges = [charge_without_dispo]
        record = Record([case])
        expunger = Expunger(record)

        assert expunger.run()

    def test_it_skips_juvenile_charges(self):
        case = CaseFactory.create(type_status=['a juvenile case', 'Closed'])
        juvenile_charge = ChargeFactory.create(case=case)
        case.charges = [juvenile_charge]

        record = Record([case])
        expunger = Expunger(record)

        assert expunger.run()
        assert expunger._skipped_charges[0] == juvenile_charge
        assert expunger.charges == []


class TestDispositionlessCharge(unittest.TestCase):

    def test_charge_is_marked_as_missing_disposition(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(case=case, statute='825.999', level='Class C traffic violation')
        print(charge.skip_analysis())
        print(charge.expungement_result.type_eligibility_reason)

        case.charges = [charge]
        expunger = Expunger(Record([case]))

        expunger.run()

        assert charge.expungement_result.type_eligibility_reason == "Disposition not found. Needs further analysis"


class TestMostRecentConvictions(unittest.TestCase):

    def test_it_sets_most_recent_conviction_from_the_last_10yrs(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(Time.LESS_THAN_TEN_YEARS_AGO, 'Convicted')
        case.charges = [mrc_charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_conviction is mrc_charge

    def test_it_sets_the_second_most_recent_conviction_within_the_last_10yrs(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(Time.TWO_YEARS_AGO, 'Convicted')
        second_mrc_charge = ChargeFactory.create()
        second_mrc_charge.disposition = Disposition(Time.LESS_THAN_TEN_YEARS_AGO, 'Convicted')

        case.charges = [second_mrc_charge, mrc_charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.second_most_recent_conviction is second_mrc_charge

    def test_it_does_not_set_mrc_when_greater_than_10yrs(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(Time.TEN_YEARS_AGO, 'Convicted')
        case.charges = [mrc_charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_conviction is None

    def test_it_does_not_set_2nd_mrc_when_greater_than_10yrs(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(Time.LESS_THAN_TEN_YEARS_AGO, 'Convicted')
        second_mrc_charge = ChargeFactory.create()
        second_mrc_charge.disposition = Disposition(Time.TEN_YEARS_AGO, 'Convicted')
        case.charges = [mrc_charge, second_mrc_charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.second_most_recent_conviction is None

    def test_mrc_and_second_mrc(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create()
        mrc_charge.disposition = Disposition(Time.TWO_YEARS_AGO, 'Convicted')
        second_mrc_charge = ChargeFactory.create()
        second_mrc_charge.disposition = Disposition(Time.LESS_THAN_TEN_YEARS_AGO, 'Convicted')
        charge = ChargeFactory.create()
        charge.disposition = Disposition(Time.TEN_YEARS_AGO, 'Convicted')
        case.charges = [charge, charge, second_mrc_charge, mrc_charge, charge, charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_conviction is mrc_charge
        assert expunger.second_most_recent_conviction is second_mrc_charge

    def test_most_recent_charge(self):
        case = CaseFactory.create()
        one_year_traffic_charge = ChargeFactory.create(name='Traffic Violation',
                                                       statute='825.999',
                                                       level='Class C traffic violation',
                                                       disposition=['Convicted', Time.ONE_YEAR_AGO])

        case.charges = [one_year_traffic_charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_charge is None

    def test_most_recent_charge_with_non_traffic_violations(self):
        case = CaseFactory.create()
        one_year_traffic_charge = ChargeFactory.create(name='Traffic Violation',
                                                       statute='825.999',
                                                       level='Class C traffic violation',
                                                       disposition=['Convicted', Time.ONE_YEAR_AGO])
        two_year_ago_dismissal = ChargeFactory.create(disposition=['Dismissed', Time.TWO_YEARS_AGO])
        three_year_ago_dismissal = ChargeFactory.create(disposition=['Dismissed', Time.THREE_YEARS_AGO])
        four_year_traffic_charge = ChargeFactory.create(name='Traffic Violation',
                                                        statute='825.999',
                                                        level='Class C traffic violation',
                                                        disposition=['Convicted', Time.FOUR_YEARS_AGO])

        case.charges = [one_year_traffic_charge, two_year_ago_dismissal, three_year_ago_dismissal, four_year_traffic_charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_charge == two_year_ago_dismissal

    def test_parking_ticket_is_not_recent_charge(self):
        case = CaseFactory.create()
        parking_ticket = ChargeFactory.create(statute='40',
                                              disposition=['Convicted', Time.ONE_YEAR_AGO])

        case.charges = [parking_ticket]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_charge is None

    def test_violation_is_not_most_recent(self):
        case = CaseFactory.create()
        mrc_charge = ChargeFactory.create(level='Violation')
        mrc_charge.disposition = Disposition(Time.LESS_THAN_TEN_YEARS_AGO, 'Convicted')
        case.charges = [mrc_charge]
        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_conviction is None

    def test_violation_and_misdemeanor_most_recent(self):
        viol_case = CaseFactory.create()
        misd_case = CaseFactory.create()

        viol_charge = ChargeFactory.create(level='Violation')
        misd_charge = ChargeFactory.create()

        viol_charge.disposition = Disposition(Time.ONE_YEAR_AGO, 'Convicted')
        misd_charge.disposition = Disposition(Time.TWO_YEARS_AGO, 'Convicted')

        viol_case.charges = [viol_charge]
        misd_case.charges = [misd_charge]

        record = Record([viol_case, misd_case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_conviction is misd_charge

    def test_recent_violation_and_nonrecent_misdemeanor(self):
        viol_case = CaseFactory.create()
        misd_case = CaseFactory.create()

        viol_charge = ChargeFactory.create(level='Violation')
        misd_charge = ChargeFactory.create()

        viol_charge.disposition = Disposition(Time.ONE_YEAR_AGO, 'Convicted')
        misd_charge.disposition = Disposition(Time.TEN_YEARS_AGO, 'Convicted')

        viol_case.charges = [viol_charge]
        misd_case.charges = [misd_charge]

        record = Record([viol_case, misd_case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_conviction is None

    def test_two_most_recent_are_violations(self):
        case = CaseFactory.create()

        viol_charge = ChargeFactory.create(level='Violation')
        viol2_charge = ChargeFactory.create(level='Violation')

        viol_charge.disposition = Disposition(Time.ONE_YEAR_AGO, 'Convicted')
        viol2_charge.disposition = Disposition(Time.TWO_YEARS_AGO, 'Convicted')

        case.charges = [viol_charge, viol2_charge]

        record = Record([case])

        expunger = Expunger(record)
        expunger.run()

        assert expunger.most_recent_conviction is viol2_charge
