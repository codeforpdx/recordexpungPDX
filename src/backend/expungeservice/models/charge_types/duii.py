from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class Duii(ChargeType):
    type_name: str = "DUII"
    expungement_rules: str = (
        """A DUII conviction is not eligible for expungement, as it is considered a traffic violation.
A DUII dismissal resulting from completion of diversion (paying a fine, victim's impact panel, drug and alcohol assessment) is also not eligible under ORS 137.225(8)(b).
HOWEVER, a DUII dismissal resulting from a Not Guilty verdict at trial, or is otherwise dismissed other than through diversion, is type-eligible like other dismissals.
Therefore, to determine whether a dismissal is eligible, ask the client whether their case was dismissed through diversion or by a Not Guilty verdict or some way other than through diversion.
"""
    )

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE, reason="Traffic offenses are ineligible under 137.225(7)(a)"
            )


@dataclass(frozen=True)
class DivertedDuii(ChargeType):
    type_name: str = "Diverted DUII"
    expungement_rules = "A DUII dismissal resulting from completion of diversion is ineligible under ORS 137.225(8)(b)."

    def type_eligibility(self, disposition):
        return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(8)(b)",)
