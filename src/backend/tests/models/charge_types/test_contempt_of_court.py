from datetime import date as date_class
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory
from tests.models.test_charge import Dispositions

def test_contempt_of_court_dismissed():
    charge_dict = {
        "case": CaseFactory.create(type_status=["Contempt of Court", "Closed"]),
        "name": "contempt of court",
        "statute": "33",
        "level": "N/A",
        "date": date_class(1901, 1, 1),
        "disposition": Dispositions.DISMISSED
    }
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, ContemptOfCourt)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"



def test_contempt_of_court_convicted():
    charge_dict = {
        "case": CaseFactory.create(type_status=["Civil Offense", "Closed"]),
        "name": "contempt of court",
        "statute": "33065",
        "level": "N/A",
        "date": date_class(1901, 1, 1),
        "disposition": Dispositions.CONVICTED
    }
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, ContemptOfCourt)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"


def test_contempt_of_court_no_disposition():
    charge_dict = {
        "case": CaseFactory.create(type_status=["Civil Offense", "Closed"]),
        "name": "contempt of court",
        "statute": "33015",
        "level": "misdemeanor",
        "date": date_class(1901, 1, 1)
    }
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, ContemptOfCourt)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"


def test_contempt_of_court_unrecognized_disposition():
    charge_dict = {
        "case": CaseFactory.create(type_status=["Civil Offense", "Closed"]),
        "name": "contempt of court",
        "statute": "33055",
        "level": "violation",
        "date": date_class(1901, 1, 1),
        "disposition": Dispositions.UNRECOGNIZED_DISPOSITION
    }
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, ContemptOfCourt)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"
