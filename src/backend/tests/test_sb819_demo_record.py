"""The SB-819 demo record exercises every Multnomah criterion end to end."""

import json

import pytest

from expungeservice.demo_records import DemoRecords
from expungeservice.models.record import Alias
from expungeservice.models.sb819 import SB819Pathway, SB819Status
from expungeservice.record_creator import RecordCreator
from expungeservice.record_summarizer import RecordSummarizer
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.util import DateWithFuture as date_class, LRUCache


@pytest.fixture
def analysis():
    record, questions = RecordCreator.build_record(
        DemoRecords.build_search_results,
        "username",
        "password",
        (Alias("sb", "819", "", ""),),
        {},
        date_class.today(),
        LRUCache(4),
    )
    assert record.errors == ()
    return RecordSummarizer.summarize(record, questions).sb819_analysis


def statuses(analysis):
    return {a.ambiguous_charge_id: a.status for a in analysis.charge_analyses}


def test_only_ineligible_multnomah_charges_are_analyzed(analysis):
    analyzed = set(statuses(analysis))
    assert "SB819-100-1" not in analyzed, "the eligible control charge should not be analyzed"
    assert "SB819-200-1" not in analyzed, "the Clackamas charge should be excluded by county"
    assert len(analyzed) == 6
    assert analysis.counties_analyzed == ("Multnomah",)


def test_a_misdemeanor_conviction_fails_the_felony_criterion(analysis):
    charge_analysis = analysis.for_charge("SB819-300-1")
    assert charge_analysis.status is SB819Status.INELIGIBLE
    assert [r.criterion.name for r in charge_analysis.blocking_results] == ["Conviction was sentenced as a felony"]


def test_aggravated_murder_fails_its_main_criterion(analysis):
    charge_analysis = analysis.for_charge("SB819-400-1")
    assert charge_analysis.status is SB819Status.INELIGIBLE
    assert [r.criterion.name for r in charge_analysis.blocking_results] == ["Conviction is not aggravated murder"]


def test_a_registerable_sex_offense_is_ruled_out_on_the_pathway(analysis):
    charge_analysis = analysis.for_charge("SB819-500-1")
    assert charge_analysis.status is SB819Status.INELIGIBLE
    assert [r.criterion.name for r in charge_analysis.blocking_results] == [
        "Conviction is not a registerable sex offense"
    ]
    assert [p.pathway for p in charge_analysis.pathway_results] == [SB819Pathway.COLLATERAL_CONSEQUENCES]


def test_charges_passing_the_main_criteria_need_more_analysis(analysis):
    for charge_id in ["SB819-600-1", "SB819-800-1", "SB819-1000-1"]:
        assert analysis.for_charge(charge_id).status is SB819Status.NEEDS_MORE_ANALYSIS


def test_an_amended_disposition_raises_the_felony_sentencing_question(analysis):
    charge_analysis = analysis.for_charge("SB819-800-1")
    questions = [r.question.text for r in charge_analysis.main_criterion_results if r.question]
    assert questions == ["Was this conviction sentenced as a felony?"]


def test_a_conditionally_registerable_offense_raises_the_reporting_question(analysis):
    """Kidnapping I registers only if the victim was under 18, which OECI does not record."""
    charge_analysis = analysis.for_charge("SB819-1000-1")
    collateral = next(p for p in charge_analysis.pathway_results if p.pathway is SB819Pathway.COLLATERAL_CONSEQUENCES)
    result = next(
        r for r in collateral.criterion_results if r.criterion.name.startswith("Conviction is not a registerable")
    )
    assert result.outcome.value == "Unknown"
    assert result.question.text == "Does this conviction require the applicant to report as a sex offender?"


def test_the_record_has_both_ineligible_and_unresolved_charges(analysis):
    sections = {status: len(items) for status, items in analysis.sections}
    assert sections[SB819Status.INELIGIBLE] == 3
    assert sections[SB819Status.NEEDS_MORE_ANALYSIS] == 3
    assert analysis.has_possibly_eligible


def test_the_analysis_is_nested_inside_the_record_summary():
    """Pins where the payload carries the analysis.

    The frontend reads it from record.summary.sb819_analysis. Serializing it as a sibling
    of "summary" instead leaves the badge with nothing to render and breaks no test that
    only checks one side of the seam.
    """
    record, questions = RecordCreator.build_record(
        DemoRecords.build_search_results,
        "username",
        "password",
        (Alias("sb", "819", "", ""),),
        {},
        date_class.today(),
        LRUCache(4),
    )
    summary = RecordSummarizer.summarize(record, questions)
    payload = json.loads(json.dumps({"record": summary}, cls=ExpungeModelEncoder))["record"]

    assert "sb819_analysis" in payload["summary"]
    assert "sb819_analysis" not in payload
    assert payload["summary"]["sb819_analysis"]["has_analyzed_charges"] is True


def test_the_analysis_serializes(analysis):
    payload = json.loads(json.dumps(analysis, cls=_AnalysisEncoder))
    assert set(payload) == {
        "counties_analyzed",
        "has_analyzed_charges",
        "has_possibly_eligible",
        "sections",
        "charges",
    }
    charge = payload["charges"]["SB819-600-1"]
    assert charge["status"] == "Needs More Analysis"
    assert len(charge["main_criteria"]) == 4
    assert len(charge["pathways"]) == 1
    collateral = next(p for p in charge["pathways"] if p["pathway"] == "Collateral Consequences")
    question = next(c["question"] for c in collateral["criteria"] if c["name"].startswith("Conviction did not"))
    assert question["if_yes"] == "SB-819 Ineligible"
    assert question["note"]


class _AnalysisEncoder(ExpungeModelEncoder):
    def default(self, o):
        from expungeservice.models.sb819 import SB819Analysis

        if isinstance(o, SB819Analysis):
            return self.sb819_analysis_to_json(o)
        return super().default(o)
