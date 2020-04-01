from expungeservice.models.disposition import Disposition
from expungeservice.record_merger import RecordMerger
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.expunger import Expunger
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.time import Time


def test_record_summarizer_multiple_cases():
    case_all_eligible = CaseFactory.create(case_number="1", balance="100.00", date_location=["1/1/1995", "Multnomah"])
    case_all_eligible.charges = [
        ChargeFactory.create(
            case_number=case_all_eligible.case_number,
            name="Theft of dignity",
            disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO),
        )
    ]

    case_partially_eligible = CaseFactory.create(
        case_number="2", balance="200.00", date_location=["1/1/1995", "Clackamas"]
    )
    case_partially_eligible.charges = [
        ChargeFactory.create(
            case_number=case_partially_eligible.case_number,
            disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO),
        ),
        ChargeFactory.create(
            case_number=case_partially_eligible.case_number,
            level="Felony Class A",
            disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO),
        ),
    ]

    case_possibly_eligible = CaseFactory.create(case_number="3", balance="300.00", date_location=["1/1/1995", "Baker"])
    case_possibly_eligible.charges = [
        ChargeFactory.create(
            case_number=case_possibly_eligible.case_number,
            level="Felony Class B",
            disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO),
        )
    ]

    case_all_ineligible = CaseFactory.create(case_number="4", balance="400.00", date_location=["1/1/1995", "Baker"])
    case_all_ineligible.charges = [
        ChargeFactory.create(
            case_number=case_all_ineligible.case_number,
            level="Felony Class A",
            disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO),
        )
    ]

    case_all_ineligible_2 = CaseFactory.create(case_number="5", date_location=["1/1/1995", "Baker"])
    case_all_ineligible_2.charges = [
        ChargeFactory.create(
            case_number=case_all_ineligible_2.case_number,
            level="Felony Class A",
            disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO),
        )
    ]
    record = Record(
        [case_all_eligible, case_partially_eligible, case_possibly_eligible, case_all_ineligible, case_all_ineligible_2]
    )
    expunger = Expunger(record)
    expunger_result = expunger.run()
    merged_record = RecordMerger.merge([record], [expunger_result])
    record_summary = RecordSummarizer.summarize(merged_record, [])

    assert record_summary.total_balance_due == 1000.00
    assert record_summary.total_cases == 5
    assert record_summary.total_charges == 6
    assert record_summary.cases_sorted["fully_eligible"] == ["1"]
    assert record_summary.cases_sorted["fully_ineligible"] == ["4", "5"]
    assert record_summary.cases_sorted["partially_eligible"] == ["2"]
    assert record_summary.cases_sorted["other"] == ["3"]

    """
    assert record_summary.county_balances["Baker"] == 700.00
    assert record_summary.county_balances["Multnomah"] == 100.00
    assert record_summary.county_balances["Clackamas"] == 200.00
    assert record_summary.eligible_charges == ["Theft of dignity", "Theft of services"]
    """


def test_record_summarizer_no_cases():
    record = Record([])
    record_summary = RecordSummarizer.summarize(record, [])

    assert record_summary.total_balance_due == 0.00
    assert record_summary.total_cases == 0
    assert record_summary.total_charges == 0
    assert record_summary.cases_sorted["fully_eligible"] == []
    assert record_summary.cases_sorted["fully_ineligible"] == []
    assert record_summary.cases_sorted["partially_eligible"] == []
    assert record_summary.cases_sorted["other"] == []
    assert record_summary.county_balances == []
    assert record_summary.eligible_charges == []
