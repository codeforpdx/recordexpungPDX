from dataclasses import dataclass

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus
from expungeservice.models.disposition import DispositionStatus


@dataclass(frozen=True)
class MarijuanaEligible(ChargeType):
    type_name: str = "Marijuana Eligible"
    expungement_rules: str = """ORS 137.226 makes eligible additional marijuana-related charges - in particular, those crimes which are now considered minor felonies or below.
    One way to identify a marijuana crime is if it has the statute section 475860.
    Also if "marijuana", "marij", or "mj" are in the charge name, we conclude it's a marijuana eligible charge (after filtering out MarijuanaIneligible charges by statute)."""

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.226")
        elif disposition.status in [DispositionStatus.UNRECOGNIZED, DispositionStatus.UNKNOWN]:
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE,
                reason="Always eligible under 137.226 (for convictions) or 137.225(1)(b) (for dismissals)",
            )


@dataclass(frozen=True)
class MarijuanaUnder21(ChargeType):
    type_name: str = "Marijuana Eligible (Below age 21)"
    expungement_rules: str = """Under ORS 137.226, marijuana convictions where the offender was under the age of 21 are eligible for conviction in a year assuming their record has no other charges."""

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 137.226")


@dataclass(frozen=True)
class MarijuanaViolation(ChargeType):
    type_name: str = "Marijuana Violation"
    expungement_rules: str = """Under 475B.401, convictions for possession of less than an ounce of marijuana are always eligible, regardless of any time eligibility restrictions that would normally apply.
    This charge type is identifiable as any marijuana charge whose level is Violation."""

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            return TypeEligibility(
                EligibilityStatus.ELIGIBLE, reason="Dismissed violations are eligible under 137.225(1)(b)"
            )
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Eligible under 475B.401")


@dataclass(frozen=True)
class MarijuanaManufactureDelivery(MarijuanaEligible):
    severity_level: str = "Felony Class C"
    type_name: str = "Marijuana Manufacture Delivery"
