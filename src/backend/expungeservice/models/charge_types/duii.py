from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


@dataclass(eq=False)
class Duii(Charge):
    type_name: str = "DUII"
    expungement_rules: str = (
"""A DUII conviction is not eligible for expungement, as it is considered a traffic violation.
A DUII dismissal resulting from completion of diversion (paying a fine, victim's impact panel, drug and alcohol assessment) is also not eligible under ORS 137.225(8)(b).
HOWEVER, a DUII dismissal resulting from a Not Guilty verdict at trial, or is otherwise dismissed other than through diversion, is type-eligible like other dismissals.
Therefore, to determine whether a dismissal is eligible, ask the client whether their case was dismissed through diversion or by a Not Guilty verdict or some way other than through diversion.
""" )

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

        unrecognized_type_eligibility = TypeEligibility(
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
            DispositionStatus.UNRECOGNIZED: unrecognized_type_eligibility,
        }
        # This that if someone adds something to DispositionStatus,
        # it won't automatically go to the Unrecognized case.
        assert len(cases) == len(DispositionStatus)
        return cases.get(self.disposition.status, unrecognized_type_eligibility)  # type: ignore
