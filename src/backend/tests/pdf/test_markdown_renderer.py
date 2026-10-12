import json

import pytest

from expungeservice.charge_creator import ChargeCreator
from expungeservice.expunger import Expunger
from expungeservice.models.charge import EditStatus
from expungeservice.models.disposition import DispositionCreator
from expungeservice.models.record import Record
from expungeservice.pdf.markdown_renderer import MarkdownRenderer
from expungeservice.record_merger import RecordMerger
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.util import DateWithFuture as date
from tests.factories.case_factory import CaseFactory
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe

@pytest.fixture
def example_record():
    return CrawlerFactory.create(
        record=JohnDoe.SINGLE_CASE_RECORD,
        cases={
            "CASEJD1": CaseDetails.CASE_WITH_REVOKED_PROBATION,
        },
    )
    
def test_render_markdown(example_record):
    record_summary = RecordSummarizer.summarize(example_record, {})
    record = json.loads(json.dumps(record_summary, cls=ExpungeModelEncoder))
    aliases = [
        {"first_name": "john", "middle_name": "", "last_name": "smith", "birth_date": "2/2/2020"},
        {"first_name": "john", "middle_name": "", "last_name": "doe", "birth_date": ""},
    ]
    source = MarkdownRenderer.to_markdown(record, aliases=aliases)
    assert source == open("./tests/pdf/expected/default.md").read()

def test_render_with_custom_header(example_record):
    record_summary = RecordSummarizer.summarize(example_record, {})
    record = json.loads(json.dumps(record_summary, cls=ExpungeModelEncoder))
    header = "# Custom Header"
    source = MarkdownRenderer.to_markdown(record, header=header)
    assert source == open("./tests/pdf/expected/custom_header.md").read()


def test_render_groups_each_section_by_county():
    def charge(case_number, index, name, level, ruling):
        # Charge ids follow the crawler's "<case number>-<n>" scheme, which the template strips to the case number.
        return ChargeCreator.create(
            f"{case_number}-{index}",
            case_number=case_number,
            name=name,
            statute="164.125",
            level=level,
            date=date(2010, 1, 1),
            disposition=DispositionCreator.create(ruling=ruling, date=date(2010, 1, 1)),
            violation_type="Offense Misdemeanor",
            location="Benton",
            balance_due_in_cents=0,
            edit_status=EditStatus.UNCHANGED,
        )[0][0]

    def case(case_number, county, balance, *charges):
        return CaseFactory.create(
            case_number=case_number,
            balance=balance,
            date_location=["1/1/1995", county],
            charges=tuple(charge(case_number, i, *spec) for i, spec in enumerate(charges, start=1)),
        )

    # Case numbers run opposite to county order so the output proves the county sort.
    record = Record(
        tuple(
            [
                case("X0001", "Multnomah", "0", ("Theft of dignity", "Misdemeanor Class A", "Dismissed")),
                case("X0002", "Clackamas", "0", ("Theft of services", "Misdemeanor Class A", "Dismissed")),
                case("X0003", "Baker", "0", ("Theft of time", "Misdemeanor Class A", "Dismissed")),
                case("X0004", "Multnomah", "0", ("Assault in the First Degree", "Felony Class A", "Convicted")),
                case("X0005", "Baker", "0", ("Assault in the Second Degree", "Felony Class A", "Convicted")),
                case("X0006", "Multnomah", "100.00", ("Trespass in the First Degree", "Misdemeanor Class A", "Dismissed")),
                case("X0007", "Baker", "200.00", ("Trespass in the Second Degree", "Misdemeanor Class A", "Dismissed")),
            ]
        )
    )
    expunger_result = Expunger.run(record)
    merged_record = RecordMerger.merge(record, record.charges, [expunger_result], [])
    record_summary = RecordSummarizer.summarize(merged_record, {})
    record_json = json.loads(json.dumps(record_summary, cls=ExpungeModelEncoder))

    source = MarkdownRenderer.to_markdown(record_json, header="# Multi County")
    assert source == open("./tests/pdf/expected/multi_county.md").read()
