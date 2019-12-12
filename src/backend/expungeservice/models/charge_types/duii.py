from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


class Duii(Charge):

    def _default_type_eligibility(self):

        if not self.disposition:
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason='Further Analysis Needed - No disposition')

        elif 'diverted' in self.disposition.ruling.lower():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason='Ineligible under 137.225(8)(b)')

        elif self.acquitted():
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason='Further Analysis Needed')

        else:
            """
            TODO: other dispositions than "convicted" are possible and are not handled here.
            See issue: https://github.com/codeforpdx/recordexpungPDX/issues/601

            TODO: reason can be expanded to "137.225(7)(a) - Traffic offenses are ineligible"
            """
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason='Ineligible under 137.225(7)(a)')
