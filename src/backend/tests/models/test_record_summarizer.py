from expungeservice.models.disposition import DispositionCreator
from expungeservice.record_merger import RecordMerger
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.expunger import Expunger
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from expungeservice.util import DateWithFuture as date


def test_record_summarizer_multiple_cases():
    case_all_eligible = CaseFactory.create(
        case_number="1",
        balance="100.00",
        date_location=["1/1/1995", "Multnomah"],
        charges=tuple(
            [
                ChargeFactory.create(
                    case_number="1",
                    name="Theft of dignity",
                    disposition=DispositionCreator.create(ruling="Convicted", date=date(2010, 1, 1)),
                )
            ]
        ),
    )

    case_partially_eligible = CaseFactory.create(
        case_number="2",
        balance="200.00",
        date_location=["1/1/1995", "Clackamas"],
        charges=tuple(
            [
                ChargeFactory.create(
                    case_number="2",
                    disposition=DispositionCreator.create(ruling="Convicted", date=date(2010, 1, 1)),
                ),
                ChargeFactory.create(
                    case_number="2",
                    level="Felony Class A",
                    disposition=DispositionCreator.create(ruling="Convicted", date=date(2010, 1, 1)),
                ),
            ]
        ),
    )

    case_possibly_eligible = CaseFactory.create(
        case_number="3",
        balance="300.00",
        date_location=["1/1/1995", "Baker"],
        charges=tuple(
            [
                ChargeFactory.create(
                    case_number="3",
                    level="Felony Class B",
                    disposition=DispositionCreator.create(ruling="Convicted", date=date(2010, 1, 1)),
                )
            ]
        ),
    )

    case_all_ineligible = CaseFactory.create(
        case_number="4",
        balance="400.00",
        date_location=["1/1/1995", "Baker"],
        charges=tuple(
            [
                ChargeFactory.create(
                    case_number="4",
                    level="Felony Class A",
                    disposition=DispositionCreator.create(ruling="Convicted", date=date(2010, 1, 1)),
                )
            ]
        ),
    )

    case_all_ineligible_2 = CaseFactory.create(
        case_number="5",
        date_location=["1/1/1995", "Baker"],
        charges=tuple(
            [
                ChargeFactory.create(
                    case_number="5",
                    level="Felony Class A",
                    disposition=DispositionCreator.create(ruling="Convicted", date=date(2010, 1, 1)),
                )
            ]
        ),
    )
    record = Record(
        tuple(
            [
                case_all_eligible,
                case_partially_eligible,
                case_possibly_eligible,
                case_all_ineligible,
                case_all_ineligible_2,
            ]
        )
    )
    expunger_result = Expunger.run(record)

    merged_record = RecordMerger.merge([record], [expunger_result], [])
    record_summary = RecordSummarizer.summarize(merged_record, {})

    assert record_summary.total_fines_due == 1000.00
    assert record_summary.total_cases == 5
    assert record_summary.total_charges == 6
    assert record_summary.charges_grouped_by_eligibility_and_case == [
        (
            "Ineligible",
            [
                (
                    "",
                    [
                        (
                            case_partially_eligible.charges[1].ambiguous_charge_id,
                            "Theft of services (CONVICTED) Charged Jan 1, 2010",
                        )
                    ],
                ),
                (
                    "",
                    [
                        (
                            case_all_ineligible.charges[0].ambiguous_charge_id,
                            "Theft of services (CONVICTED) Charged Jan 1, 2010",
                        )
                    ],
                ),
                (
                    "",
                    [
                        (
                            case_all_ineligible_2.charges[0].ambiguous_charge_id,
                            "Theft of services (CONVICTED) Charged Jan 1, 2010",
                        )
                    ],
                ),
            ],
        ),
        (
            "Eligible Now If Balance Paid",
            [
                (
                    "Multnomah 1 – $100.0",
                    [
                        (
                            case_all_eligible.charges[0].ambiguous_charge_id,
                            "Theft of dignity (CONVICTED) Charged Jan 1, 2010",
                        )
                    ],
                ),
                (
                    "Baker 3 – $300.0",
                    [
                        (
                            case_possibly_eligible.charges[0].ambiguous_charge_id,
                            "Theft of services (CONVICTED) Charged Jan 1, 2010",
                        )
                    ],
                ),
            ],
        ),
        (
            "Eligible Now If Balance Paid on case with Ineligible charge",
            [
                (
                    "Clackamas 2 – $200.0",
                    [
                        (
                            case_partially_eligible.charges[0].ambiguous_charge_id,
                            "Theft of services (CONVICTED) Charged Jan 1, 2010",
                        )
                    ],
                ),
            ],
        ),
    ]

    assert (
        next(county.total_fines_due for county in record_summary.county_fines if county.county_name == "Multnomah")
        == 100
    )
    assert (
        next(county.total_fines_due for county in record_summary.county_fines if county.county_name == "Clackamas")
        == 200
    )
    assert (
        next(county.total_fines_due for county in record_summary.county_fines if county.county_name == "Baker") == 700
    )


def test_record_summarizer_no_cases():
    record = Record(tuple([]))
    record_summary = RecordSummarizer.summarize(record, {})

    assert record_summary.total_fines_due == 0.00
    assert record_summary.total_cases == 0
    assert record_summary.total_charges == 0
    assert record_summary.county_fines == []
    assert record_summary.charges_grouped_by_eligibility_and_case == []
