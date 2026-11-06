"""The Collateral Consequences pathway (MCDA Information Sheet, pages 4 to 5)."""

from expungeservice.models.sb819 import (
    SB819Outcome,
    SB819Pathway,
    SB819PathwayResult,
    SB819Status,
)
from expungeservice.sb819_criteria import multnomah

from tests.factories.sb819_factory import SB819Factory


def by_name(results):
    return {r.criterion.name: r for r in results}


def test_a_registerable_sex_offense_blocks_collateral_consequences():
    record, case, charge = SB819Factory.single_charge_record(
        name="Rape in the Second Degree", statute="163.365", level="Felony Class B"
    )
    result = SB819PathwayResult.build(
        SB819Pathway.COLLATERAL_CONSEQUENCES, multnomah.collateral_consequences(charge, case, record)
    )
    assert result.status is SB819Status.INELIGIBLE
    assert [r.criterion.name for r in result.blocking_results] == [multnomah.NOT_REGISTERABLE_SEX_OFFENSE.name]


def test_an_offense_registerable_only_on_unrecorded_facts_is_asked_about():
    record, case, charge = SB819Factory.single_charge_record(
        name="Kidnapping in the First Degree", statute="163.235", level="Felony Class A"
    )
    results = by_name(multnomah.collateral_consequences(charge, case, record))
    result = results[multnomah.NOT_REGISTERABLE_SEX_OFFENSE.name]
    assert result.outcome is SB819Outcome.UNKNOWN
    assert result.question is not None


def test_sentence_completion_is_asked_rather_than_read_from_the_record():
    """OECI carries no post-prison supervision or probation end date."""
    record, case, charge = SB819Factory.single_charge_record()
    results = by_name(multnomah.collateral_consequences(charge, case, record))
    result = results[multnomah.SENTENCE_COMPLETED.name]
    assert result.outcome is SB819Outcome.UNKNOWN
    assert result.question.if_no is SB819Status.INELIGIBLE


def test_the_domestic_violence_question_carries_the_juvenile_exception():
    record, case, charge = SB819Factory.single_charge_record()
    results = by_name(multnomah.collateral_consequences(charge, case, record))
    question = results[multnomah.NO_DOMESTIC_VIOLENCE.name].question
    assert question.if_yes is SB819Status.INELIGIBLE
    assert "juvenile" in question.note and "intimate partner" in question.note


def test_the_narrative_criteria_are_reported_without_a_question():
    record, case, charge = SB819Factory.single_charge_record()
    results = by_name(multnomah.collateral_consequences(charge, case, record))
    for criterion in [multnomah.SUBSTANTIAL_REHABILITATION, multnomah.MANIFEST_HARDSHIP]:
        assert results[criterion.name].question is None


def test_a_pathway_with_every_question_open_needs_more_analysis():
    record, case, charge = SB819Factory.single_charge_record()
    result = SB819PathwayResult.build(
        SB819Pathway.COLLATERAL_CONSEQUENCES, multnomah.collateral_consequences(charge, case, record)
    )
    assert result.status is SB819Status.NEEDS_MORE_ANALYSIS
    assert result.blocking_results == ()
