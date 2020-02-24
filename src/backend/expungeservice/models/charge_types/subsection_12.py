from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class Subsection12(Charge):
    type_name: str = "Subsection 12"
    expungement_rules: str = (
        """Subsection 12 names 13 felony statutes that are eligible (or conditionally eligible, in the case of 163.525, Incest).
The subsection describes an irregular criterion for eligibility: Conviction of these charges is eligible unless the court or DA provide reason they should *not* be expunged. This is in contrast to most expungements, for which the person needs to "convince" the court that expungement is in the interest of justice.
The subsection also says that the listed felonies need to otherwise meet eligibility under the other expungement rules. In practice, this actually is never considered and the listed felonies are considered all eligible. Overall, the subsection is fairly unclear, but the State has generally settled on expunging any of these charges.
Dismissals are eligible under 137.225(1)(b)."""
    )
    eligible_sections = [
        # In order listed in the subsection
        # Incest and "attempt" statutes are commented out; see below
        "163535",  # (Abandonment of a child)
        # "163175",  # (Attempted Assault II)
        # "163165",  # (Assault III) -superceded by section 6, for the special case of assault of a minor.
        "163275",  # (Coercion)
        # "163205",  # (Criminal mistreatment I) superceded by section 6, for the special case of mistreatment of a minor or a senior.
        # "162165",  # (Attempted escape in the first degree)
        # "163525", (Incest), see below
        "166165",  # (Intimidation in the first degree)
        # "163225",  # (Attempted Kidnapping in the second degree)
        # "164405",  # (Attempted Robbery in the second degree)
        "164395",  # (Robbery in the third degree)
        "162185",  # (Supplying contraband)
        "166220",  # (Unlawful use of weapon)
    ]
    conditionally_eligible_sections = ["163525"]  # (Incest), conditional that the victim was at least 18 years of age.

    """
    The following statutes are eligible if tried as an Attempt charge.
    But if this is the case, the actual charge will be filed under a different statute number, meaning this set of statutes never provides additional information for eligibility.

    TODO: We should figure out what the statutes for attempt are so that we can identify those charges and apply this subsection.

    eligible_attempt_sections = [
        "163175",
        "162165",
        "163225",
        "164405",
    ]
    """

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            if self._section == "163525":
                return TypeEligibility(
                    EligibilityStatus.NEEDS_MORE_ANALYSIS,
                    reason="Incest is possibly eligible under 137.225(12), if the victim was at least 18 years of age.",
                )
            elif self._section in self.eligible_sections:
                return TypeEligibility(
                    EligibilityStatus.ELIGIBLE,
                    reason="Eligible under 137.225(12). This subsection also describes more lenient expungement criteria than other subsections.",
                )
