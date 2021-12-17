from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


@dataclass(frozen=True)
class ParkingTicket(ChargeType):
    type_name: str = "Parking Ticket"
    expungement_rules: str = """Parking Ticket convictions are not eligible. ORS 137.225(7)(a) specifically prohibits expungement of convicted traffic offenses.
The eligibility of a dismissed traffic violation is subject to some debate. 137.225(1)(d) says that "At any time after an acquittal or a dismissal...an arrested, cited or charged person may apply to the court in the county in which the person was arrested, cited or charged, for entry of an order setting aside the record of the arrest, citation or charge." A driving offense probably qualifies as a citation under any definition of the word.
However, DAs will probably object to filing for these, at least initially, based off their understanding of the previous version of the law, and their relationships with the other parts of the State, and the practical administrative burdens this would place on those systems.
Most directly, it’s not clear that the local municipal systems have a good way of expunging traffic tickets, dismissed or not.
As such, petitioners filing to expunge dismissed traffic tickets may receive pushback and have their petition rejected, and do so at their own risk."""
    blocks_other_charges: bool = False
    severity_level: str = "Violation"

    def type_eligibility(self, disposition):
        if ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(7)(a)")
        elif ChargeUtil.dismissed(disposition):
            return TypeEligibility(
                EligibilityStatus.NEEDS_MORE_ANALYSIS,
                reason="Dismissed violations are eligible under 137.225(1)(b) but administrative reasons may make this difficult to expunge.",
            )

    def hidden_in_record_summary(self, disposition):
        return True
