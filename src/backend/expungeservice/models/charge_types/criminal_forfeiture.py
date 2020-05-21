from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class CriminalForfeiture(Charge):
    type_name: str = "Criminal Forfeiture"
    expungement_rules: str = (
        """Criminal Forfeiture is a proceeding in which the government attempts to prove that certain property is the fruit of a crime, and therefore may be seized by the State. This is a civil proceeding and the criminal expungement statute does not specifically refer to it. However, this charge is usually tried in the same proceedings as the underlying criminal case, and prosecutions of this charge type receive criminal procedure protections. As such, there is a reason to think that these charges are type-eligible.
Therefore, best practice would be not to file on these charges standing alone, but if the case on which the charge appears is otherwise eligible for expungement, then add this charge to the list of charges to be expunged.
"""
    )
    blocks_other_charges: bool = False

    def _type_eligibility(self):
        return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible by omission from statute")
