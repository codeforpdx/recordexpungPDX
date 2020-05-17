from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class JuvenileCharge(Charge):
    type_name: str = "Juvenile"
    expungement_rules: str = (
        """Juvenile records do not follow the general expungement rules. They are governed by a completely separate statute, ORS 419A.260 and 419A.262. We do not include them in our expungement analysis because information related to the cases is generally not available online, and the process for expunging these records is very different. Below is a summary of the juvenile expungement law.

In general, Under 419A.262(8), anyone can file for a motion for expungement in juvenile cases. The motion will then go to a contested hearing. Then “the juvenile court, after a hearing when the matter is contested, may order expunction of all or any part of the person’s record if it finds that to do so would be in the best interests of the person and the public.”

The hearing will not be contested if a person meets certain narrow criteria:

    1. At least five years have elapsed since the date of the person’s most recent termination;
    2. Since the date of the most recent termination, the person has not been convicted of a felony or a Class A misdemeanor
    3. No proceedings seeking a criminal conviction or an adjudication in a juvenile court are pending against the person
    4. The person is not within the jurisdiction of any juvenile court on the basis of a petition alleging an act or behavior as defined in ORS 419B.100
    5. The juvenile department is not aware of any pending investigation of the conduct of the person by any law enforcement agency.

Additionally, under 419A.262(3)(B), cases for prostitution are automatically eligible for expungement if the person was 18 years or younger at the time of the conduct, and under 419A.262(9), “Romeo and Juliet” cases are eligible for expungement.

The list of charges in ORS 419A.260(1)(d)(J) excludes certain charges from expungement eligibility. These charges generally would not be juvenile records since Oregon’s “Measure 11” requires the defendants in such cases to be charged as adults."""
    )
    blocks_other_charges: bool = False

    def _type_eligibility(self):
        return TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, reason="Potentially eligible under 419A.262")
