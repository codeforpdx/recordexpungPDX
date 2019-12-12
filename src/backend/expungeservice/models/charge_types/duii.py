from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


class Duii(Charge):

    def _default_type_eligibility(self):

        if not self.disposition:
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason='Further Analysis Needed - No disposition')

        elif self.disposition.status == DispositionStatus.DIVERTED:
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason='137.225(8)(b) - Diverted DUII charges are ineligible')

        elif self.convicted():

            """
            TODO: reason can be expanded to "137.225(7)(a) - Traffic offenses are ineligible"
            """
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason='137.225(7)(a) - Traffic offenses are ineligible')

        elif self.acquitted():
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason='Further Analysis Needed - Dismissed charge may have been Diverted')

        else:
            return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason='Further Analysis Needed - Unrecognized ruling')
