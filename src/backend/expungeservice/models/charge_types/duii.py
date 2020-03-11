from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass
class Duii(Charge):
    type_name: str = "DUII"
    expungement_rules: str = (
        """A DUII conviction is not eligible for expungement, as it is considered a traffic violation.
A DUII dismissal resulting from completion of diversion (paying a fine, victim's impact panel, drug and alcohol assessment) is also not eligible under ORS 137.225(8)(b).
HOWEVER, a DUII dismissal resulting from a Not Guilty verdict at trial, or is otherwise dismissed other than through diversion, is type-eligible like other dismissals.
Therefore, to determine whether a dismissal is eligible, ask the client whether their case was dismissed through diversion or by a Not Guilty verdict or some way other than through diversion.
"""
    )

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)",)
        elif self.convicted():
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE, reason="137.225(7)(a) - Traffic offenses are ineligible"
            )


@dataclass
class DivertedDuii(Charge):
    type_name: str = "Diverted DUII"

    def _type_eligibility(self):
        """
        DUII charges can be diverted, and in some cases the Disposition will
        reflect this and in others it will say Dismissed.  We need to handle
        both possibilities.
        """
        if self.dismissed():
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE, reason="137.225(8)(b) - Diverted DUIIs are ineligible",
            )
        elif self.convicted():
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE, reason="137.225(7)(a) - Traffic offenses are ineligible"
            )
