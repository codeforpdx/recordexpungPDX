from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


@dataclass
class MarijuanaEligible(Charge):
    type_name: str = "Marijuana Eligible"
    expungement_rules: str = """ORS 137.226 makes eligible additional marijuana-related charges - in particular, those crimes which are now considered minor felonies or below.
    One way to identify a marijuana crime is if it has the statute section 475860.
    Also if "marijuana", "marij", or "mj" are in the charge name, we conclude it's a marijuana eligible charge (after filtering out MarijuanaIneligible charges by statute)."""
    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.226")
        elif not self.disposition or self.disposition.status == DispositionStatus.UNRECOGNIZED:
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE,
                reason="Always eligible under 137.226 (for convictions) or 137.225(1)(b) (for dismissals)",
            )