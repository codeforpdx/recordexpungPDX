from datetime import date
from dateutil.relativedelta import relativedelta


class TimeAnalyzer:

    TWENTY_YEARS_AGO = date.today() + relativedelta(years=-20)
    TWENTY_YEARS = 20
    TEN_YEARS = 10
    THREE_YEARS = 3

    def __init__(self, expunger):
        self._expunger = expunger

    def evaluate(self, charges):
        if self._expunger.most_recent_conviction:
            self._mark_all_charges_ineligible_using_mrc_date(charges, 'Time-ineligible under 137.225(7)(b)', self.TEN_YEARS)
            self._check_mrc_time_eligibility()
        elif self._expunger.most_recent_dismissal and self._more_than_one_recent_acquittal_from_another_case():
            self._mark_all_charges_ineligible_using_mrd_date(charges, 'Recommend sequential expungement of arrests')
            self._mark_all_mrd_case_related_charges_eligible()
        else:
            TimeAnalyzer._mark_all_charges_eligible(charges)

        self._evaluate_class_b_felonies()

    def _mark_all_charges_ineligible_using_mrc_date(self, charges, reason, years):
        eligibility_date = self._expunger.most_recent_conviction.disposition.date + relativedelta(years=years)
        for charge in charges:
            charge.set_time_ineligible(reason, eligibility_date)

    def _check_mrc_time_eligibility(self):
        if self._expunger.second_most_recent_conviction:
            eligibility_date = self._expunger.second_most_recent_conviction.disposition.date + relativedelta(years=self.TEN_YEARS)
            self._expunger.most_recent_conviction.set_time_ineligible('Multiple convictions within last ten years', eligibility_date)
        elif self._most_recent_conviction_is_greater_than_three_years_old():
            self._expunger.most_recent_conviction.set_time_eligible()
        else:
            eligibility_date = self._expunger.most_recent_conviction.disposition.date + relativedelta(years=self.THREE_YEARS)
            self._expunger.most_recent_conviction.set_time_ineligible('Most recent conviction is less than three years old', eligibility_date)

    def _most_recent_conviction_is_greater_than_three_years_old(self):
        three_years_ago = date.today() + relativedelta(years=-3)
        return self._expunger.most_recent_conviction.disposition.date <= three_years_ago

    def _more_than_one_recent_acquittal_from_another_case(self):
        return self._expunger.num_acquittals - len(self._expunger.most_recent_dismissal.case()().charges) > 0

    def _mark_all_charges_ineligible_using_mrd_date(self, charges, reason):
        eligibility_date = self._expunger.most_recent_dismissal.date + relativedelta(years=+self.THREE_YEARS)
        for charge in charges:
            charge.set_time_ineligible(reason, eligibility_date)

    def _mark_all_mrd_case_related_charges_eligible(self):
        for charge in self._expunger.most_recent_dismissal.case()().charges:
            charge.set_time_eligible('Recommend sequential expungement of arrests')

    def _evaluate_class_b_felonies(self):
        if self._expunger.most_recent_charge and self._expunger.most_recent_charge.disposition.date > self.TWENTY_YEARS_AGO:
            for charge in self._expunger.class_b_felonies:
                charge.set_time_ineligible('Time-ineligible under 137.225(5)(a)(A)(i)',
                                           self._expunger.most_recent_charge.disposition.date + relativedelta(
                                               years=self.TWENTY_YEARS))

    @staticmethod
    def _mark_all_charges_eligible(charges):
        for charge in charges:
            charge.set_time_eligible()
