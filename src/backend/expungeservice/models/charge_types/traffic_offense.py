from dataclasses import dataclass
from typing import Any

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class TrafficOffense(ChargeType):
    type_name: str = "Traffic Offense"
    expungement_rules: Any = (
        "A conviction for a State or municipal traffic offense is not eligible for expungement under ORS 137.225(7)(a).",
        "Common convictions under this category include:",
        (
            "ul",
            (
                "Reckless Driving",
                "Driving While Suspended",
                "Driving Under the Influence of Intoxicants",
                "Failure to Perform Duties of a Driver",
                "Giving False Information to a Police Officer (when in a car)",
                "Fleeing/Attempting to Elude a Police Officer",
                "Possession of a Stolen Vehicle",
            ),
        ),
        "Notably, Unauthorized Use of a Vehicle is not considered a traffic offense.",
        "A dismissed traffic offense that is of charge level misdemeanor or higher, other than a Diverted DUII, is identified as a Dismissed Criminal Charge, and is thus eligible.",
    )

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
