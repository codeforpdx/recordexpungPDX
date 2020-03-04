from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus



@dataclass(eq=False)
class ContemptOfCourt(Charge):
    """ This is a civil offense. However it may be eligible by charge level(misdemeanor or
    convicted violation). Statutes for contempt include 33.015, 33.055, and 33.065 """

    type_name: str = "Contempt of Court"
    expungement_rules: str = (
        """ Eligible if level Misdemeanor (convicted or dismissed) 137.225(5)(b), Violation (convicted only) 137.225(5)(d)

            Not eligible if level Violation (dismissed), or if level N/A as it is a civil offense """
    )

    def _type_eligibility(self):
        if self.level != 'N/A':
            if 'violation' in self.level.lower() and self.convicted():
                return TypeEligibility(EligibilityStatus.ELIGIBLE, reason='Eligible under 137.225(5)(d) (for convicted violations)')
            elif 'violation' in self.level.lower() and self.dismissed():
                return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(1)(b) ommission from statute (for dismissals)")

            if 'misdemeanor' in self.level.lower():
                return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Misdemeanors are always eligible under 137.225(5)(b) for convictions, or 137.225(1)(b) for dismissals")

        return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")

    def blocks_other_charges(self):
        return False
