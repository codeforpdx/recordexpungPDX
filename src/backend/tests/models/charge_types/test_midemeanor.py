from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_misdemeanor():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Criminal Trespass in the Second Degree"
    charge_dict["statute"] = "164.245"
    charge_dict["level"] = "Misdemeanor Class C"
    charge_dict["disposition"] = None

    misdemeanor_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(misdemeanor_charge, Misdemeanor)
    assert misdemeanor_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        misdemeanor_charge.expungement_result.type_eligibility.reason
        == "Misdemeanors are always eligible under 137.225(5)(b) for convictions, or 137.225(1)(b) for dismissals"
    )


def test_misdemeanor_164043():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Theft in the third degree"
    charge_dict["statute"] = "164.043"
    charge_dict["level"] = "Misdemeanor Class C"
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, Misdemeanor)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"


def test_misdemeanor_164125():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Theft of services"
    charge_dict["statute"] = "164.125"
    charge_dict["level"] = "Misdemeanor Class A"
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, Misdemeanor)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"


def test_drug_free_zone_variance_misdemeanor():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "	Drug Free Zone Variance"
    charge_dict["statute"] = "14B20060"
    charge_dict["level"] = "Misdemeanor Unclassified"
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, Misdemeanor)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"
