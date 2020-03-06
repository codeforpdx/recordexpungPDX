from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus



@dataclass(eq=False)
class ContemptOfCourt(Charge):

    type_name: str = "Contempt of Court"
    expungement_rules: str = (
        """ This is a civil offense that is always ineligible regardless of level / conviction status """
    )

    def _type_eligibility(self):
        return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")

    def blocks_other_charges(self):
        return False
