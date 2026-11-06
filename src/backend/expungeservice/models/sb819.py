"""Data structures for SB-819 limiting criteria analysis.

SB 819 (2021) lets a District Attorney jointly petition with a convicted person to
reconsider a conviction or sentence. Each county's DA publishes limiting criteria that
gate which applications the office will screen. These structures describe one county's
criteria and the result of applying them to a single charge.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

from typing_extensions import Protocol


class SB819Status(str, Enum):
    POSSIBLY_ELIGIBLE = "Possibly SB-819 Eligible"
    NEEDS_MORE_ANALYSIS = "Needs More Analysis"
    INELIGIBLE = "SB-819 Ineligible"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


# Most severe last, so max() over this ordering picks the worst status and min() the best.
STATUS_SEVERITY = {
    SB819Status.POSSIBLY_ELIGIBLE: 0,
    SB819Status.NEEDS_MORE_ANALYSIS: 1,
    SB819Status.INELIGIBLE: 2,
}

# The order the sections appear in the SB-819 view.
STATUS_DISPLAY_ORDER = [
    SB819Status.POSSIBLY_ELIGIBLE,
    SB819Status.NEEDS_MORE_ANALYSIS,
    SB819Status.INELIGIBLE,
]


def best_status(statuses) -> SB819Status:
    return min(statuses, key=lambda status: STATUS_SEVERITY[status])


def worst_status(statuses) -> SB819Status:
    return max(statuses, key=lambda status: STATUS_SEVERITY[status])


class SB819Pathway(str, Enum):
    COLLATERAL_CONSEQUENCES = "Collateral Consequences"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class SB819Determination(str, Enum):
    """How a criterion is settled."""

    OECI = "OECI"  # From record data.
    QUESTION = "Question"  # Asked of the client; the answer is not in the record.
    PART_TWO = "Part 2"  # Narrative showing, assessed outside this analysis.

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class SB819Scope(str, Enum):
    """What a criterion is a fact about, and therefore how often it is asked.

    A case-scope criterion is a fact about a prosecution, so it is asked once however many
    convictions the case carries.
    """

    CASE = "case"
    CHARGE = "charge"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class SB819Outcome(str, Enum):
    PASSED = "Passed"
    FAILED = "Failed"
    UNKNOWN = "Unknown"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


@dataclass(frozen=True)
class SB819Question:
    """A yes/no question the client answers, displayed with both outcomes.

    These are display-only. Unlike the expungement questions in models/record.py, they
    carry no selection and never round-trip to the backend for re-analysis.
    """

    text: str
    if_yes: SB819Status
    if_no: SB819Status
    note: str = ""


# Only these two kinds of criterion count toward a status. The other is settled by documents
# the applicant assembles later, so nothing the volunteer can read or ask resolves it.
# Counting it would pin the pathway at Needs More Analysis permanently; such criteria are
# presented as instructions instead.
SCREENABLE_DETERMINATIONS = (SB819Determination.OECI, SB819Determination.QUESTION)


@dataclass(frozen=True)
class SB819Criterion:
    key: str
    name: str
    description: str
    citation: str
    determination: SB819Determination
    pathway: Optional[SB819Pathway] = None  # None marks a main criterion.
    scope: SB819Scope = SB819Scope.CHARGE
    # The question that defines who a pathway is for. The pathway's other questions are put
    # to the client only once this one is answered in the pathway's favor, so a volunteer
    # is not asked about domestic violence for an applicant still under supervision.
    is_gate: bool = False

    @property
    def is_screenable(self) -> bool:
        return self.determination in SCREENABLE_DETERMINATIONS


@dataclass(frozen=True)
class SB819CriterionResult:
    criterion: SB819Criterion
    outcome: SB819Outcome
    explanation: str
    question: Optional[SB819Question] = None


def _resolve_outcomes(results: Tuple[SB819CriterionResult, ...]) -> SB819Status:
    """A pathway fails on any failed criterion, and is unresolved on any unknown one.

    Criteria that are not screenable take no part; see SCREENABLE_DETERMINATIONS.
    """
    outcomes = [r.outcome for r in results if r.criterion.is_screenable]
    if SB819Outcome.FAILED in outcomes:
        return SB819Status.INELIGIBLE
    elif SB819Outcome.UNKNOWN in outcomes:
        return SB819Status.NEEDS_MORE_ANALYSIS
    else:
        return SB819Status.POSSIBLY_ELIGIBLE


def disqualifying_results(results) -> Tuple["SB819CriterionResult", ...]:
    """The failed criteria that bar a pathway, in the order they were evaluated.

    Criteria that are not screenable take no part in a status, so they cannot be what
    barred it.
    """
    return tuple(r for r in results if r.criterion.is_screenable and r.outcome == SB819Outcome.FAILED)


@dataclass(frozen=True)
class SB819PathwayResult:
    pathway: SB819Pathway
    status: SB819Status
    criterion_results: Tuple[SB819CriterionResult, ...]

    @staticmethod
    def build(pathway: SB819Pathway, results: List[SB819CriterionResult]) -> "SB819PathwayResult":
        return SB819PathwayResult(pathway, _resolve_outcomes(tuple(results)), tuple(results))

    @property
    def blocking_results(self) -> Tuple[SB819CriterionResult, ...]:
        return disqualifying_results(self.criterion_results)

    @property
    def open_questions(self) -> Tuple[SB819CriterionResult, ...]:
        return tuple(r for r in self.criterion_results if r.question)


def resolve_charge_status(main_status: SB819Status, pathway_statuses) -> SB819Status:
    """A failed main criterion ends the analysis; no pathway can rescue it.

    Otherwise the charge is only as good as its best pathway, and never better than its
    main criteria.
    """
    if main_status == SB819Status.INELIGIBLE:
        return SB819Status.INELIGIBLE
    if not pathway_statuses:
        return main_status
    return worst_status([main_status, best_status(pathway_statuses)])


@dataclass(frozen=True)
class SB819ChargeAnalysis:
    ambiguous_charge_id: str
    case_number: str
    charge_name: str
    status: SB819Status
    main_criterion_results: Tuple[SB819CriterionResult, ...]
    pathway_results: Tuple[SB819PathwayResult, ...]

    @property
    def blocking_results(self) -> Tuple[SB819CriterionResult, ...]:
        """Every criterion that disqualifies the charge, main criteria first."""
        main = disqualifying_results(self.main_criterion_results)
        return main + tuple(r for pathway in self.pathway_results for r in pathway.blocking_results)

    @property
    def open_questions(self) -> Tuple[SB819CriterionResult, ...]:
        main = tuple(r for r in self.main_criterion_results if r.question)
        return main + tuple(r for pathway in self.pathway_results for r in pathway.open_questions)

    @property
    def instructions(self) -> Tuple[SB819CriterionResult, ...]:
        """Criteria the applicant or the District Attorney settles later, not questions."""
        return tuple(
            r for pathway in self.pathway_results for r in pathway.criterion_results if not r.criterion.is_screenable
        )


@dataclass(frozen=True)
class SB819Analysis:
    charge_analyses: Tuple[SB819ChargeAnalysis, ...] = ()
    counties_analyzed: Tuple[str, ...] = ()

    @property
    def has_analyzed_charges(self) -> bool:
        return len(self.charge_analyses) > 0

    @property
    def has_possibly_eligible(self) -> bool:
        """Needs More Analysis counts: an unresolved charge is by definition still possible."""
        return any(analysis.status != SB819Status.INELIGIBLE for analysis in self.charge_analyses)

    @property
    def sections(self) -> List[Tuple[SB819Status, List[SB819ChargeAnalysis]]]:
        return [(status, [a for a in self.charge_analyses if a.status == status]) for status in STATUS_DISPLAY_ORDER]

    def for_charge(self, ambiguous_charge_id: str) -> Optional[SB819ChargeAnalysis]:
        return next((a for a in self.charge_analyses if a.ambiguous_charge_id == ambiguous_charge_id), None)


class PathwayBuilder(Protocol):
    """Takes (charge, case, record) and returns that pathway's criterion results.

    mypy binds a Callable-typed dataclass field as a method when it is read through an
    instance, and the call then fails to type-check. A Protocol field is read as a plain
    attribute.
    """

    def __call__(self, charge, case, record) -> List[SB819CriterionResult]:
        ...


@dataclass(frozen=True)
class SB819Ruleset:
    """One county's published SB-819 limiting criteria."""

    county: str
    main_criteria: PathwayBuilder
    pathways: Dict[SB819Pathway, PathwayBuilder]

    def analyze(self, charge, case, record) -> SB819ChargeAnalysis:
        main_results = self.main_criteria(charge, case, record)
        main_status = _resolve_outcomes(tuple(main_results))

        if main_status == SB819Status.INELIGIBLE:
            # A failed main criterion ends the analysis; no pathway can rescue it.
            return SB819ChargeAnalysis(
                ambiguous_charge_id=charge.ambiguous_charge_id,
                case_number=charge.case_number,
                charge_name=charge.name,
                status=SB819Status.INELIGIBLE,
                main_criterion_results=tuple(main_results),
                pathway_results=(),
            )

        pathway_results = [
            SB819PathwayResult.build(pathway, builder(charge, case, record))
            for pathway, builder in self.pathways.items()
        ]
        return SB819ChargeAnalysis(
            ambiguous_charge_id=charge.ambiguous_charge_id,
            case_number=charge.case_number,
            charge_name=charge.name,
            status=resolve_charge_status(main_status, [r.status for r in pathway_results]),
            main_criterion_results=tuple(main_results),
            pathway_results=tuple(pathway_results),
        )
