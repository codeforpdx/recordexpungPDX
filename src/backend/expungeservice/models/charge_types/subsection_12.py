from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class Subsection12(Charge):
    type_name: str = "Subsection 12"
    expungement_rules: str = (
        """Subsection (12) names 13 felony statutes that are interpreted as eligible (or conditionally eligible, in the case of 163.525, Incest).
The subsection describes an irregular criterion for eligibility: Conviction of these charges is eligible unless the court or DA provide reason they should *not* be expunged. This is in contrast to most expungements, for which the person needs to "convince" the court that expungement is in the interest of justice.
The subsection also says that the listed felonies need to otherwise meet eligibility under the other expungement rules. In practice, this actually is never considered and the listed felonies are considered all eligible. Overall, the subsection is confusing and seems a little nonsensical, but the State has generally settled on expunging any of these charges.
Applicable subsections: 137.225(12) for convictions; 137.225(1)(b) for dismissals."""
    )

    # TODO: the elif convicted(): block needs to be added here pending the open issue for a Subsection 12 overhaul.
    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        else:
            if self.statute == "163525":
                return TypeEligibility(
                    EligibilityStatus.NEEDS_MORE_ANALYSIS,
                    reason="Incest is possibly eligible under 137.225(12), if the victim was at least 18 years of age.",
                )
            else:
                return TypeEligibility(
                    EligibilityStatus.ELIGIBLE,
                    reason="Eligible under 137.225(12). This subsection is interpreted to override any conflicting subsections.",
                )
