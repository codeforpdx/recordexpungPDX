from dataclasses import dataclass
from typing import Any

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class MarijuanaIneligible(ChargeType):
    type_name: str = "Marijuana Ineligible"
    expungement_rules: Any = (
        "ORS 137.226 makes eligible additional marijuana-related charges - in particular, those crimes which are now considered minor felonies or below. However, there are certain marijuana-related crimes which are still considered major felonies. These are:",
        (
            "ul",
            (
                "475B.359 Arson incident to manufacture of cannabinoid extract in first degree",
                "475B.367 Causing another person to ingest marijuana",
                "475B.371 Administration to another person under 18 years of age",
                "167.262: Use of minor in controlled substance or marijuana item offense",
            ),
        ),
    )

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.226")
