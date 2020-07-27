from dataclasses import dataclass
from typing import Any

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class FelonyClassB(ChargeType):
    type_name: str = "Felony Class B"
    expungement_rules: Any = (
        """Class B felony dismissals are always eligible under 137.225(5)(a).
Class B felony convictions are generally eligible but subject to additional restrictions compared to other charge types, as listed in 137.225(5)(a).
The extra restrictions are:""",
        (
            "ul",
            (
                "An extended time restriction: the class B felony is ineligible until 20 years after its date of conviction.",
                "The class B felony is ineligible if the person has been arrested or convicted for any crime, other than a traffic violation, following the date of the class B felony conviction.",
                "If the charge is also classified as a Person Crime it is ineligible.",
            ),
        ),
        "If a class B felony is eligible under any other subsection of the statute, that eligibility takes precedences and the extra restrictions here are ignored. The alternate positive criteria that can apply to B felonies are:",
        (
            "ul",
            (
                "If the charge is a drug crime for which the underlying substance is marijuana, it follows the typical time restrictions for a minor criminal charge.",
                "Some class B felonies fall under Subsection 6 which takes precendence over 137.225(5)(a).",
                "If the class B felony is punishable as a misdemeanor, it is eligible under 137.225(5)(b).",
            ),
        ),
    )

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE,
                reason="Convictions that fulfill the conditions of 137.225(5)(a) are eligible",
            )
