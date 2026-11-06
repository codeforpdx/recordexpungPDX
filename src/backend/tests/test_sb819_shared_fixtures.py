"""The half of the shared resolution table that the backend is responsible for.

src/shared/sb819ResolutionFixtures.json states how criteria compose into a status. The rules
are applied here in Python and again in TypeScript when a volunteer answers a question, so
both suites execute this file and a disagreement fails a test.

The answer scenarios are the frontend's alone, since answers are only ever applied in the
browser. Everything downstream of an answer is shared, and that is what the outcome
scenarios pin.
"""

import json
from pathlib import Path
from typing import List

import pytest

from expungeservice.models.sb819 import (
    disqualifying_results,
    SB819Criterion,
    SB819CriterionResult,
    SB819Determination,
    SB819Outcome,
    SB819PathwayResult,
    SB819Status,
    _resolve_outcomes,
    resolve_charge_status,
)

FIXTURES = Path(__file__).resolve().parents[2] / "shared" / "sb819ResolutionFixtures.json"


def load_scenarios():
    data = json.loads(FIXTURES.read_text())
    return [pytest.param(s, id=s["name"]) for s in data["outcome_scenarios"]]


def build_result(entry) -> SB819CriterionResult:
    criterion = SB819Criterion(
        key=entry["key"],
        name=entry["key"],
        description="",
        citation="",
        determination=SB819Determination(entry["determination"]),
    )
    return SB819CriterionResult(criterion=criterion, outcome=SB819Outcome(entry["outcome"]), explanation="")


def test_the_shared_fixture_file_is_present():
    assert FIXTURES.exists(), f"shared resolution fixtures missing at {FIXTURES}"


@pytest.mark.parametrize("scenario", load_scenarios())
def test_outcomes_resolve_as_the_shared_table_says(scenario):
    main_results = [build_result(e) for e in scenario["main"]]
    main_status = _resolve_outcomes(tuple(main_results))

    expected = scenario["expect"]

    if expected.get("pathways_not_evaluated"):
        assert main_status == SB819Status.INELIGIBLE
        assert resolve_charge_status(main_status, []) == SB819Status(expected["charge"])
        return

    pathway_statuses = []
    barred: List[str] = []
    for pathway in scenario["pathways"]:
        results = [build_result(e) for e in pathway["criteria"]]
        status = _resolve_outcomes(tuple(results))
        assert status == SB819Status(expected["pathways"][pathway["pathway"]]), pathway["pathway"]
        pathway_statuses.append(status)
        barred += [r.criterion.key for r in disqualifying_results(tuple(results))]

    assert resolve_charge_status(main_status, pathway_statuses) == SB819Status(expected["charge"])

    if "disqualifying" in expected:
        assert barred == expected["disqualifying"]


def test_pathway_results_agree_with_the_bare_resolver():
    """SB819PathwayResult.build is the production entry point and must not diverge."""
    scenario = json.loads(FIXTURES.read_text())["outcome_scenarios"][0]
    results = [build_result(e) for e in scenario["pathways"][0]["criteria"]]
    from expungeservice.models.sb819 import SB819Pathway

    built = SB819PathwayResult.build(SB819Pathway.COLLATERAL_CONSEQUENCES, results)
    assert built.status == _resolve_outcomes(tuple(results))
