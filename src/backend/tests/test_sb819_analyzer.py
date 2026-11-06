"""Scope filtering and roll-up from the main criteria and the pathway."""

from expungeservice.models.expungement_result import ChargeEligibilityStatus
from expungeservice.models.sb819 import SB819Pathway, SB819Status
from expungeservice.sb819_analyzer import SB819Analyzer

from tests.factories.sb819_factory import SB819Factory


def analyze(**kwargs):
    record, _, _ = SB819Factory.single_charge_record(**kwargs)
    return SB819Analyzer.build(record)


# --- what enters the analysis ----------------------------------------------


def test_an_ineligible_multnomah_conviction_is_analyzed():
    assert len(analyze().charge_analyses) == 1


def test_a_charge_outside_multnomah_is_excluded():
    """No ruleset is implemented for other counties, and marking those charges ineligible
    would read as a decision the DA has not made."""
    analysis = analyze(location="Clackamas")
    assert analysis.charge_analyses == ()
    assert analysis.counties_analyzed == ()


def test_a_dismissed_charge_is_excluded_even_when_expungement_cannot_reach_it():
    """A dismissed traffic violation is ineligible for expungement, and is not a conviction.
    SB 819 sets aside convictions only, so it has no place in the analysis."""
    from expungeservice.models.disposition import DispositionCreator
    from expungeservice.util import DateWithFuture as date_class

    analysis = analyze(
        name="Failure to Obey Traffic Control Device",
        statute="811.265",
        level="Violation Class B",
        violation_type="Offense Violation",
        disposition=DispositionCreator.create(date=date_class.today(), ruling="Dismissed"),
    )
    assert analysis.charge_analyses == ()


def test_a_convicted_traffic_violation_is_excluded_like_the_record_summary_excludes_it():
    """A ticket is a conviction expungement cannot reach, and it is not an SB 819 case. The
    record summary hides these charge types, and the view follows the summary."""
    from expungeservice.models.disposition import DispositionCreator
    from expungeservice.util import DateWithFuture as date_class

    analysis = analyze(
        name="Speeding",
        statute="811.111",
        level="Violation Class C",
        violation_type="Offense Violation",
        disposition=DispositionCreator.create(date=date_class.today(), ruling="Convicted"),
    )
    assert analysis.charge_analyses == ()


def test_a_charge_that_is_eligible_now_is_excluded():
    assert analyze(eligibility=ChargeEligibilityStatus.ELIGIBLE_NOW).charge_analyses == ()


def test_a_charge_that_will_be_eligible_later_is_excluded():
    """A charge eligible on a future date is expungeable under ORS 137.225, so expungement
    is the required route and SB 819 does not apply."""
    assert analyze(eligibility=ChargeEligibilityStatus.WILL_BE_ELIGIBLE).charge_analyses == ()


def test_charges_needing_more_expungement_analysis_are_excluded():
    assert analyze(eligibility=ChargeEligibilityStatus.NEEDS_MORE_ANALYSIS).charge_analyses == ()


def test_a_charge_ineligible_only_if_restitution_is_owed_is_excluded():
    assert analyze(eligibility=ChargeEligibilityStatus.INELIGIBLE_IF_RESTITUTION_OWED).charge_analyses == ()


def test_a_deleted_charge_is_excluded():
    from dataclasses import replace

    from expungeservice.models.charge import EditStatus

    record, case, charge = SB819Factory.single_charge_record()
    deleted = replace(charge, edit_status=EditStatus.DELETE)
    record = SB819Factory.record([SB819Factory.case([deleted])])
    assert SB819Analyzer.build(record).charge_analyses == ()


# --- roll-up ----------------------------------------------------------------


def test_a_failed_main_criterion_ends_the_analysis():
    analysis = analyze(
        name="Driving Under the Influence of Intoxicants", statute="813.010", level="Misdemeanor Class A"
    )
    charge_analysis = analysis.charge_analyses[0]
    assert charge_analysis.status is SB819Status.INELIGIBLE
    assert charge_analysis.pathway_results == ()
    assert len(charge_analysis.blocking_results) == 1


def test_a_charge_passing_the_main_criteria_needs_more_analysis():
    charge_analysis = analyze().charge_analyses[0]
    assert charge_analysis.status is SB819Status.NEEDS_MORE_ANALYSIS
    assert charge_analysis.blocking_results == ()


def test_a_failed_pathway_criterion_rules_the_charge_out():
    """A registerable sex offense bars Collateral Consequences, and the main criteria are
    still reported so the reader can see the charge got that far."""
    charge_analysis = analyze(
        name="Rape in the Second Degree", statute="163.365", level="Felony Class B"
    ).charge_analyses[0]
    assert charge_analysis.status is SB819Status.INELIGIBLE
    assert [r.criterion.name for r in charge_analysis.blocking_results] == [
        "Conviction is not a registerable sex offense"
    ]
    assert len(charge_analysis.main_criterion_results) == 4


def test_the_pathway_is_evaluated():
    charge_analysis = analyze().charge_analyses[0]
    assert [p.pathway for p in charge_analysis.pathway_results] == [SB819Pathway.COLLATERAL_CONSEQUENCES]


def test_an_uncertain_main_criterion_holds_the_charge_at_needs_more_analysis():
    from expungeservice.models.disposition import DispositionCreator
    from expungeservice.util import DateWithFuture as date_class

    record, case, charge = SB819Factory.single_charge_record(
        level="Felony Class A",
        disposition=DispositionCreator.create(date=date_class.today(), ruling="Convicted", amended=True),
    )
    charge_analysis = SB819Analyzer.build(record).charge_analyses[0]
    assert charge_analysis.status is SB819Status.NEEDS_MORE_ANALYSIS
    assert any(r.question for r in charge_analysis.main_criterion_results)


# --- summary shape ----------------------------------------------------------


def test_needs_more_analysis_counts_as_possibly_eligible():
    """An unresolved charge is by definition still possible, so the badge reads positively."""
    analysis = analyze()
    assert analysis.charge_analyses[0].status is SB819Status.NEEDS_MORE_ANALYSIS
    assert analysis.has_possibly_eligible


def test_an_entirely_ineligible_record_reports_no_possibly_eligible_charges():
    analysis = analyze(name="Aggravated Murder", statute="163.095", level="Felony Class A")
    assert analysis.has_analyzed_charges
    assert not analysis.has_possibly_eligible


def test_sections_are_ordered_for_display():
    sections = analyze().sections
    assert [status for status, _ in sections] == [
        SB819Status.POSSIBLY_ELIGIBLE,
        SB819Status.NEEDS_MORE_ANALYSIS,
        SB819Status.INELIGIBLE,
    ]


def test_an_empty_record_reports_nothing_analyzed():
    analysis = SB819Analyzer.build(SB819Factory.record([]))
    assert not analysis.has_analyzed_charges
    assert not analysis.has_possibly_eligible
