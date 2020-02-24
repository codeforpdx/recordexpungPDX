from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.subsection_12 import Subsection12
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_subsection_12_dismissed():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Abandonment of a child"
    charge_dict["statute"] = "163.535"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.DISMISSED
    subsection_12_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"
    )

def test_subsection_12_163535():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Abandonment of a child"
    charge_dict["statute"] = "163.535"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_12_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(12). This subsection also describes more lenient expungement criteria than other subsections."
    )

def test_subsection_12_163275():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Coercion"
    charge_dict["statute"] = "163.275"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_12_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(12). This subsection also describes more lenient expungement criteria than other subsections."
    )

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(12). This subsection also describes more lenient expungement criteria than other subsections."
    )

def test_subsection_12_163525():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Incest"
    charge_dict["statute"] = "163.525"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_12_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason
        == "Incest is possibly eligible under 137.225(12), if the victim was at least 18 years of age."
    )


def test_subsection_12_166165():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Intimidation in the first degree"
    charge_dict["statute"] = "166.165"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_12_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(12). This subsection also describes more lenient expungement criteria than other subsections."
    )

def test_subsection_12_164395():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Robbery in the third degree"
    charge_dict["statute"] = "164.395"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_12_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(12). This subsection also describes more lenient expungement criteria than other subsections."
    )

def test_subsection_12_162185():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Supplying contraband"
    charge_dict["statute"] = "162.185"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_12_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(12). This subsection also describes more lenient expungement criteria than other subsections."
    )

def test_subsection_12_166220():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Unlawful use of weapon"
    charge_dict["statute"] = "166.220"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_12_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(12). This subsection also describes more lenient expungement criteria than other subsections."
    )

# Test that sub-chapters are not compared when not necessary.
def test_subsection_12_charge_that_includes_sub_chapter():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Unlawful use of weapon"
    charge_dict["statute"] = "166.220(1)(b)"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Dispositions.CONVICTED
    subsection_12_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(subsection_12_charge, Subsection12)
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        subsection_12_charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(12). This subsection also describes more lenient expungement criteria than other subsections."
    )
