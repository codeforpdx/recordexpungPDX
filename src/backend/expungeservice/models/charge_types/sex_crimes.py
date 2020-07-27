from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class SexCrime(ChargeType):
    type_name: str = "Sex Crime"
    expungement_rules: str = (
        """Sex Crimes are type-ineligible for expungement other than a narrow exception for "Romeo and Juliet" cases.
For further detail, see 137.225(6)(a)"""
    )

    statutes = [
        "163365",  # Rape II
        "163375",  # Rape I
        "163395",  # Sodomy II
        "163405",  # Sodomy I
        "163408",  # Sexual Penetration II
        "163411",  # Sexual Penetration I
        "163413",  # Purchasing Sex with a Minor
        "163425",  # Sexual Abuse II
        "163427",  # Sexual Abuse I
        "163432",  # Online Sexual Corruption of a Child II
        "163433",  # Online Sexual Corruption of a Child I
        "163452",  # Custodial Sexual Misconduct in the First Degree
        "163454",  # Custodial sexual misconduct in the second degree
        "163465",  # Felony Public Indecency
        "163467",  # Private indecency
        "163472",  # Unlawful Dissemination of Initimate Image
        "163476",  # Unlawfully being in a location where children regularly congregate
        "163479",  # Unlawful Contact with a Child
        "163670",  # Using Child In Display of Sexual Conduct
        "163684",  # Encouraging Child Sex Abuse I
        "163686",  # Encouraging Child Sex Abuse II
        "163687",  # Encouraging child sexual abuse in the third degree
        "163688",  # Possession of Material Depicting Sexually Explicit Conduct of Child I
        "163689",  # Possession of Material Depicting Sexually Explicit Conduct of Child II
        "163693",  # Failure to report Child Pornography
        "167012",  # Promoting prostitution
        "167017",  # Compelling prostitution
        "167057",  # Luring a minor
        "167062",  # Sadomasochistic abuse or sexual conduct in live show
        "167075",  # Exhibiting an obscene performance to a minor
        "167080",  # Displaying obscene materials to minors
        "167090",  # Publicly displaying nudity or sex for advertising purposes
    ]

    # Romeo and Juliet exception; If a person is convicted of one of the following, and follows certain other
    # requirements which are not identifiable in eCourts, they are eligible.
    romeo_and_juliet_exceptions = [
        "163355",  # Rape in the third degree
        "163385",  # Sodomy in the third degree
        "163415",  # Sexual Abuse in the Third Degree
        "163435",  # Contributing to the sexual deliquency of a minor
        "163445",  # Sexual Misconduct
    ]

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(6)(a)")


@dataclass(frozen=True)
class RomeoAndJulietNMASexCrime(ChargeType):
    type_name: str = "Young Offender Sex Crime"
    expungement_rules: str = """In some cases, a statutory rape charge may be eligible for a young offender. The required conditions are listed in 137.225(6)(f).
        Please contact michael@qiu-qiulaw.com for manual analysis."""

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE,
                reason="Possibly meets requirements under 137.225(6)(f) - Email michael@qiu-qiulaw.com with subject line '6F' for free and confidential further analysis",
            )


@dataclass(frozen=True)
class RomeoAndJulietIneligibleSexCrime(ChargeType):
    type_name: str = "Young Offender Sex Crime"
    expungement_rules: str = """See other entry for this charge type"""

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(
                EligibilityStatus.INELIGIBLE, reason="Fails to meet requirements under 137.225(6)(f)"
            )
