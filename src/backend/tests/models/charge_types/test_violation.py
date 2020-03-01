from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.violation import Violation

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_violation():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Viol Treatment"
    charge_dict["statute"] = "1615662"
    charge_dict["level"] = "Violation Unclassified"
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, Violation)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(d)"
