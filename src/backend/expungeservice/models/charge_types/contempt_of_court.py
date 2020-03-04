from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus



@dataclass(eq=False)
class ContemptOfCourt(Charge):
    """ This is a civil offense """

    type_name: str = "Contempt of Court"
    expungement_rules: str = (
        """ Ineligible by ommission from statute. """
    )

    def _type_eligibility(self):
        return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")

    def blocks_other_charges(self):
        return False
