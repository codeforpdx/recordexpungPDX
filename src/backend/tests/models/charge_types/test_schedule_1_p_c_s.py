from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.schedule_1_p_c_s import Schedule1PCS

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_pcs_475854():
    pcs_charge = ChargeFactory.create(
        name="Unlawful possession of heroin",
        statute="475.854",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(pcs_charge, Schedule1PCS)
    assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"


def test_pcs_475874():
    pcs_charge = ChargeFactory.create(
        name="Unlawful possession of 3,4-methylenedioxymethamphetamine",
        statute="475.874",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(pcs_charge, Schedule1PCS)
    assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"


def test_pcs_475884():
    pcs_charge = ChargeFactory.create(
        name="Unlawful possession of cocaine",
        statute="475.884",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(pcs_charge, Schedule1PCS)
    assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"


def test_pcs_475894():
    pcs_charge = ChargeFactory.create(
        name="Unlawful possession of methamphetamine",
        statute="475.894",
        level="Misdemeanor Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(pcs_charge, Schedule1PCS)
    assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"


def test_pcs_475992():
    pcs_charge = ChargeFactory.create(
        name="Poss Controlled Sub 2", statute="4759924B", level="Felony Class C", disposition=Dispositions.CONVICTED
    )

    assert isinstance(pcs_charge, Schedule1PCS)
    assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"


def test_pcs_dismissed_violation():
    for level in (
        "Class C Violation",
        "Class c violation",
        "Class B Violation",
        "Class B violation",
        "Class D Violation",
        "Class D violation",
    ):
        pcs_charge = ChargeFactory.create(
            name="Poss Controlled Sub 2", statute="4759924B", disposition=Dispositions.DISMISSED, level=level
        )
        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            pcs_charge.expungement_result.type_eligibility.reason
            == "Dismissed violations are ineligible by omission from statute"
        )


def test_pcs_dismissed_nonviolation():
    pcs_charge = ChargeFactory.create(
        name="Poss Controlled Sub 2", statute="4759924B", level="Felony Class C", disposition=Dispositions.DISMISSED
    )  # also test non-violation
    assert isinstance(pcs_charge, Schedule1PCS)
    assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert pcs_charge.expungement_result.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"
