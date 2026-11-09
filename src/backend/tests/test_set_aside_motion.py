"""A case with a set-aside motion already filed, from the merged record through to the paperwork."""
# The parser side is in tests/parser/test_case_parser.py.
import json
from dataclasses import replace
from unittest.mock import MagicMock

from expungeservice.charge_creator import ChargeCreator
from expungeservice.expunger import Expunger
from expungeservice.form_filling import CaseResults, FormFilling
from expungeservice.models.case import SetAsideMotion, SetAsideMotionStatus
from expungeservice.models.charge import EditStatus
from expungeservice.models.disposition import DispositionCreator
from expungeservice.models.expungement_result import ChargeEligibilityStatus
from expungeservice.models.record import Record
from expungeservice.pdf.markdown_renderer import MarkdownRenderer
from expungeservice.record_creator import RecordCreator
from expungeservice.record_merger import RecordMerger
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.util import DateWithFuture as date, LRUCache
from tests.factories.case_factory import CaseFactory
from tests.test_edit_results import search

FILED = SetAsideMotion(SetAsideMotionStatus.FILED, date(2026, 2, 18), None)
DENIED = SetAsideMotion(SetAsideMotionStatus.DENIED, date(2026, 2, 18), date(2026, 8, 24))
WITHDRAWN = SetAsideMotion(SetAsideMotionStatus.WITHDRAWN, date(2024, 11, 4), date(2024, 12, 2))

USER_INFO = {
    "full_name": "",
    "date_of_birth": "",
    "phone_number": "",
    "mailing_address": "",
    "city": "",
    "state": "",
    "zip_code": "",
    "email_address": "",
}


def charge(case_number, index, name, level, location):
    # Charge ids follow the crawler's "<case number>-<n>" scheme, which the PDF strips to the case number.
    return ChargeCreator.create(
        f"{case_number}-{index}",
        case_number=case_number,
        name=name,
        statute="164.125",
        level=level,
        date=date(2010, 1, 1),
        disposition=DispositionCreator.create(ruling="Convicted", date=date(2010, 1, 1)),
        violation_type="Offense Misdemeanor",
        location=location,
        balance_due_in_cents=0,
        edit_status=EditStatus.UNCHANGED,
    )[0][0]


def case(case_number, motion=None, with_ineligible=False, location="Multnomah"):
    charges = [charge(case_number, 1, "Theft of services", "Misdemeanor Class A", location)]
    if with_ineligible:
        charges.append(charge(case_number, 2, "Arson", "Felony Class A", location))
    built = CaseFactory.create(case_number=case_number, date_location=["1/1/1995", location], charges=tuple(charges))
    return replace(built, summary=replace(built.summary, set_aside_motion=motion))


def merged(*cases):
    record = Record(tuple(cases))
    return RecordMerger.merge(record, record.charges, [Expunger.run(record)], [])


def labels(record):
    return {
        charge.ambiguous_charge_id: charge.expungement_result.charge_eligibility.label
        for a_case in record.cases
        for charge in a_case.charges
    }


def test_an_open_motion_parks_the_eligible_charges_and_leaves_ineligible_ones_alone():
    record = merged(case("1", FILED, with_ineligible=True), case("2"))
    assert labels(record) == {"1-1": "Motion Previously Filed", "1-2": "Ineligible", "2-1": "Eligible Now"}
    status = record.cases[0].charges[0].expungement_result.charge_eligibility.status
    assert status == ChargeEligibilityStatus.MOTION_FILED


def test_a_denied_or_withdrawn_motion_changes_no_eligibility():
    record = merged(case("1", DENIED), case("2", WITHDRAWN))
    assert labels(record) == {"1-1": "Eligible Now", "2-1": "Eligible Now"}


def test_the_summary_puts_the_motion_section_first():
    record = merged(case("1", FILED, with_ineligible=True), case("2"))
    sections = RecordSummarizer.summarize(record, {}).charges_grouped_by_eligibility_and_case
    assert [label for label, _ in sections] == ["Motion Previously Filed", "Ineligible", "Eligible Now"]
    assert sections[0][1] == [("", [("1-1", "Theft of services (CONVICTED) Charged Jan 1, 2010")])]


def test_the_motion_is_serialized_with_its_dates():
    record = merged(case("1", DENIED), case("2"))
    cases = json.loads(json.dumps(record, cls=ExpungeModelEncoder))["cases"]
    assert cases[0]["set_aside_motion"] == {
        "status": "Denied",
        "filed_date": "Feb 18, 2026",
        "resolved_date": "Aug 24, 2026",
    }
    assert cases[1]["set_aside_motion"] is None


def edit_motion(edit):
    record, _ = RecordCreator.build_record(
        search("two_cases_two_charges_each"),
        "username",
        "password",
        (),
        {"X0002": {"summary": {"edit_status": "UPDATE", "set_aside_motion": edit}}},
        date.today(),
        LRUCache(4),
    )
    return record.cases[1].summary


def test_the_editor_sets_a_motion_with_its_dates():
    summary = edit_motion({"status": "Denied", "filed_date": "2/18/2026", "resolved_date": "8/24/2026"})
    assert summary.set_aside_motion == DENIED
    assert summary.edit_status == EditStatus.UPDATE


def test_the_editor_reads_no_resolved_date_for_a_filed_motion():
    summary = edit_motion({"status": "Filed", "filed_date": "2/18/2026", "resolved_date": "8/24/2026"})
    assert summary.set_aside_motion == FILED


def test_the_editor_clears_a_motion():
    assert edit_motion({"status": "None", "filed_date": "", "resolved_date": ""}).set_aside_motion is None


def test_a_case_with_an_open_motion_gets_no_paperwork():
    record = merged(case("1", FILED), case("2"))
    results = [CaseResults.build(a_case, USER_INFO, "") for a_case in record.cases]
    assert [r.is_expungeable_now for r in results] == [False, True]
    assert FormFilling.counties_with_cases_to_expunge(results) == ["Multnomah"]


def test_the_osp_sheet_lists_every_skipped_case():
    record = merged(case("1", FILED), case("2"), case("3", FILED, location="Lane"))
    record_summary = RecordSummarizer.summarize(record, {})
    assert FormFilling.open_motion_warnings(record_summary) == [
        "Case 1 has a set-aside motion filed on Feb 18, 2026 and was skipped.",
        "Case 3 has a set-aside motion filed on Feb 18, 2026 and was skipped.",
    ]


def test_a_denied_motion_is_a_sentence_on_the_new_motion_for_its_case():
    record = merged(case("1", DENIED), case("2", WITHDRAWN), case("3"))
    sentences = [CaseResults.build(a_case, USER_INFO, "").set_aside_motion_warning for a_case in record.cases]
    assert sentences == [
        "A motion to set aside this case was filed on Feb 18, 2026 and denied on Aug 24, 2026. "
        "Review that motion before filing this one.",
        "A motion to set aside this case was filed on Nov 4, 2024 and withdrawn on Dec 2, 2024. "
        "Review that motion before filing this one.",
        "",
    ]


def test_the_warnings_sheet_carries_both_kinds_of_warning():
    mapper = MagicMock()
    values = {
        "(set_aside_motion_warning)": "A motion to set aside this case was filed on Feb 18, 2026 and denied.",
        "(open_motion_warnings)": ["Case 3 has a set-aside motion filed on Feb 18, 2026 and was skipped."],
    }
    mapper.get.side_effect = values.get
    text = FormFilling._generate_warnings_text(mapper)
    assert text == (
        "# Warnings from RecordSponge  \n"
        "Do not submit this page to the District Attorney's office.  \n \n"
        "\\* A motion to set aside this case was filed on Feb 18, 2026 and denied.  \n"
        "\\* Case 3 has a set-aside motion filed on Feb 18, 2026 and was skipped.  \n"
    )


def rendered(record):
    record_json = json.loads(json.dumps(RecordSummarizer.summarize(record, {}), cls=ExpungeModelEncoder))
    return MarkdownRenderer.to_markdown(record_json, header="# Report")


def test_the_summary_pdf_has_a_section_for_open_motions():
    markdown = rendered(merged(case("1", FILED), case("2")))
    start = markdown.index("### Motion Previously Filed")
    section = markdown[start : markdown.index("#### Disclaimer")]
    assert "No new motion is needed for them" in section
    assert "#### Multnomah\n - 1: Theft of services (CONVICTED) Charged Jan 1, 2010\n" in section
    assert markdown.index("### Charges Eligible Now") < start


def test_the_summary_pdf_prints_a_resolved_motion_once_under_its_case():
    markdown = rendered(merged(case("1", DENIED, with_ineligible=True), case("2")))
    note = "A motion to set aside case 1 was filed on Feb 18, 2026 and denied on Aug 24, 2026."
    assert markdown.count(note) == 1
    # Case 1 appears in two sections; the note follows its first charges and is not repeated.
    assert markdown.index(" - 1: Arson") < markdown.index(note) < markdown.index("### Future Eligible Charges")


def test_a_record_without_motions_renders_no_section_or_note():
    markdown = rendered(merged(case("1"), case("2")))
    assert "Motion Previously Filed" not in markdown
    assert "A motion to set aside" not in markdown
