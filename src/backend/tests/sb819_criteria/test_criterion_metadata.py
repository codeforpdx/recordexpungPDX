"""Scope and key carried by every criterion, which the browser relies on.

Scope decides how often a question is asked. It lives here rather than in the frontend
because whether a fact concerns the person, the case, or the conviction is legal knowledge,
and a list of criterion names in TypeScript would drift the first time one is reworded.
"""

from expungeservice.models.sb819 import SB819Determination, SB819Scope
from expungeservice.sb819_criteria import multnomah

ALL_CRITERIA = [v for k, v in vars(multnomah).items() if k.isupper() and hasattr(v, "determination")]


def keys_at(scope):
    return sorted(c.key for c in ALL_CRITERIA if c.scope is scope)


def test_every_criterion_carries_a_key_and_a_scope():
    for criterion in ALL_CRITERIA:
        assert criterion.key, criterion.name
        assert isinstance(criterion.scope, SB819Scope), criterion.name


def test_keys_are_unique():
    keys = [c.key for c in ALL_CRITERIA]
    assert len(keys) == len(set(keys))


def test_the_one_fact_about_a_prosecution_is_asked_once_per_case():
    assert keys_at(SB819Scope.CASE) == ["sentence-completed"]


def test_everything_else_is_asked_per_conviction():
    assert len(keys_at(SB819Scope.CHARGE)) == len(ALL_CRITERIA) - 1


def test_only_the_two_unsettleable_criteria_are_unscreenable():
    unscreenable = sorted(c.key for c in ALL_CRITERIA if not c.is_screenable)
    assert unscreenable == ["manifest-hardship", "substantial-rehabilitation"]


def test_unscreenable_criteria_carry_no_question():
    """They are instructions, not questions, so nothing offers a Yes or No for them."""
    for criterion in ALL_CRITERIA:
        if not criterion.is_screenable:
            assert criterion.determination is SB819Determination.PART_TWO


def test_the_payload_exposes_what_the_browser_resolves_with():
    import json

    from expungeservice.demo_records import DemoRecords
    from expungeservice.models.record import Alias
    from expungeservice.record_creator import RecordCreator
    from expungeservice.record_summarizer import RecordSummarizer
    from expungeservice.serializer import ExpungeModelEncoder
    from expungeservice.util import DateWithFuture as date_class, LRUCache

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
    charge = payload["summary"]["sb819_analysis"]["charges"]["SB819-600-1"]

    every_criterion = charge["main_criteria"] + [c for p in charge["pathways"] for c in p["criteria"]]
    for entry in every_criterion:
        for field in ["key", "scope", "is_gate", "is_screenable"]:
            assert field in entry, f"{field} missing from {entry['name']}"

    assert [c["key"] for c in every_criterion if c["is_gate"]] == ["sentence-completed"]


def test_a_gate_is_a_single_question_that_defines_its_pathway():
    """The browser holds a pathway's other questions back until its gate is met.

    That only makes sense for one criterion per pathway, and only for one the client
    answers: a gate settled from the record would never open anything.
    """
    gates = [c for c in ALL_CRITERIA if c.is_gate]
    assert {c.key for c in gates} == {"sentence-completed"}
    pathways = [c.pathway for c in gates]
    assert len(pathways) == len(set(pathways)), "two gates on one pathway"
    for gate in gates:
        assert gate.pathway is not None, f"{gate.key}: a main criterion gates every pathway already"
        assert gate.determination is SB819Determination.QUESTION, f"{gate.key}: a gate must be a question"


def test_every_criterion_is_explained_on_the_rules_page():
    """The sheet a lawyer audits must account for every rule the software applies."""
    from expungeservice.sb819_criteria.logic_sheet import HOW_DETERMINED, all_criteria

    keys = {c.key for c in all_criteria(multnomah)}
    assert keys - set(HOW_DETERMINED) == set(), "criteria with no operational note"
    assert set(HOW_DETERMINED) - keys == set(), "notes for criteria that no longer exist"


def test_the_rules_page_numbers_every_criterion_exactly_once():
    from expungeservice.endpoints.sb819_rules import _logic_sheet

    sheet = _logic_sheet()
    listed = [
        block["key"] for section in sheet["sections"] for block in section["blocks"] if block["kind"] == "criterion"
    ]
    assert len(listed) == len(set(listed)), "a criterion appears twice on the sheet"
    assert set(listed) == {c.key for c in ALL_CRITERIA}

    numbered = [
        block["number"]
        for section in sheet["sections"]
        for block in section["blocks"]
        if block["kind"] == "criterion" and block["screened"]
    ]
    assert len(numbered) == len(set(numbered)), "two criteria share a number"
    assert all(numbered), "a screened criterion has no number"


def test_the_rules_page_quotes_only_questions_the_software_asks():
    from expungeservice.endpoints.sb819_rules import _logic_sheet
    from expungeservice.sb819_criteria.logic_sheet import all_criteria

    sheet = _logic_sheet()
    asked = {c.key for c in all_criteria(multnomah) if c.determination is SB819Determination.QUESTION}
    quoted = {q["name"] for q in sheet["questions"]}
    by_name = {c.name for c in all_criteria(multnomah) if c.key in asked}
    # Every criterion put as a question is quoted, and nothing else is invented.
    assert by_name <= quoted
    # The record-determined criteria that fall back to a question are quoted too, which
    # holds only while the demo record the sheet reads from exercises each fallback.
    sometimes_asked = {
        "Conviction was sentenced as a felony",
        "Conviction is not a registerable sex offense",
    }
    assert sometimes_asked <= quoted, f"not quoted: {sometimes_asked - quoted}"
    assert len(sheet["questions"]) == 4
