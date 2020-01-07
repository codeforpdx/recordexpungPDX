from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


class Duii(Charge):
    def _default_type_eligibility(self):
        """
        DUII charges can be diverted, and in some cases the Disposition will
        reflect this and in others it will say Dismissed.  We need to handle
        both possibilities.
        """
        dismissed_type_eligibility = TypeEligibility(
            EligibilityStatus.NEEDS_MORE_ANALYSIS,
            reason="Further Analysis Needed - Dismissed charge may have been Diverted",
        )

        unknown_type_eligibility = TypeEligibility(
            EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Further Analysis Needed - Unrecognized ruling"
        )

        convicted_type_eligibility = TypeEligibility(
            EligibilityStatus.INELIGIBLE, reason="137.225(7)(a) - Traffic offenses are ineligible"
        )

        diverted_type_eligibility = TypeEligibility(
            EligibilityStatus.INELIGIBLE, reason="137.225(8)(b) - Diverted DUII charges are ineligible"
        )

        cases = {
            DispositionStatus.CONVICTED: convicted_type_eligibility,
            DispositionStatus.DISMISSED: dismissed_type_eligibility,
            DispositionStatus.NO_COMPLAINT: dismissed_type_eligibility,
            DispositionStatus.DIVERTED: diverted_type_eligibility,
            DispositionStatus.UNKNOWN: unknown_type_eligibility,
        }
        # This that if someone adds something to DispositionStatus,
        # it won't automatically go to the Unknown case.
        assert len(cases) == len(DispositionStatus)
        return cases.get(self.disposition.status, unknown_type_eligibility)  # type: ignore
