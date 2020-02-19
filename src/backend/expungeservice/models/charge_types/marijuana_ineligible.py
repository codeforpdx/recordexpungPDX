from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class MarijuanaIneligible(Charge):
    type_name: str = "Marijuana Ineligible"
    expungement_rules: str = """ORS 137.226 makes eligible additional marijuana-related charges - in particular, those crimes which are now considered minor felonies or below. However, there are certain marijuana-related crimes which are still considered major felonies. These are:

475B.359 Arson incident to manufacture of cannabinoid extract in first degree
475B.367 Causing another person to ingest marijuana
475B.371 Administration to another person under 18 years of age
167.262: Use of minor in controlled substance or marijuana item offense"""

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.226")
