from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
from expungeservice.record_merger import RecordMerger


def test_felony_unclassified_charge():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminal Forfeiture", statute="CH666", level="Felony Unclassified", disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Ineligible by omission from statute ⬥ Convictions that fulfill the conditions of 137.225(5)(a) are eligible ⬥ Eligible under 137.225(5)(b)"
    )


def test_felony_class_a_charge():
    felony_class_a_convicted = ChargeFactory.create(
        name="Unlawful Possession of a Weapon by a Prison Inmate",
        statute="166.275",
        level="Felony Unclassified",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(felony_class_a_convicted, FelonyClassA)
    assert felony_class_a_convicted.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert felony_class_a_convicted.type_eligibility.reason == "Ineligible by omission from statute"
