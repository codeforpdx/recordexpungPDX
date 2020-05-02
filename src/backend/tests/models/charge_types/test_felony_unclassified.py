from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
from expungeservice.record_merger import RecordMerger


def test_felony_unclassified_charge():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Criminal Forfeiture",
        statute="CH666",
        level="Felony Unclassified",
        disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Ineligible by omission from statute ⬥ Convictions that fulfill the conditions of 137.225(5)(a) are eligible ⬥ Eligible under 137.225(5)(b)"
    )
