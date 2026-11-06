"""Renders a county's SB-819 criteria as a numbered logic sheet.

The sheet is what a lawyer audits instead of the code. It is generated from the criteria,
so it cannot describe a rule the software does not apply or omit one it does; tests hold
every criterion to appearing on it exactly once.

Everything except HOW_DETERMINED is read from the criteria themselves. That mapping records
the operational test for each criterion, which lives in the functions rather than the
metadata, and every criterion must appear in it.
"""

import re
from typing import Dict, List

from expungeservice.models.sb819 import (
    SB819Criterion,
    SB819Determination,
    SB819Pathway,
    SB819Question,
    SB819Scope,
)

# The exact test applied to the record, in the terms a reader can check against OECI.
HOW_DETERMINED: Dict[str, str] = {
    "in-multnomah": "The case county recorded in OECI is Multnomah.",
    "not-expungeable": (
        "RecordSponge's own analysis of ORS 137.225 and 137.226 returns Ineligible for this "
        "conviction. A conviction that becomes eligible on a future date is not treated as "
        "ineligible, because expungement remains the required route for it. Only convictions "
        "are considered: a dismissed charge that expungement cannot reach, such as a dismissed "
        "traffic violation, is not a conviction and is left out."
    ),
    "sentenced-as-felony": (
        "The charge level recorded in OECI contains the word felony, which includes Felony "
        "Class A, B and C and Felony Unclassified. Asked of the client instead where the "
        "disposition was amended, was to a lesser charge, or reduced the charge to a "
        "violation, because the level the charge was sentenced at may then be lower than the "
        "level it was charged at."
    ),
    "not-aggravated-murder": (
        "The statute is ORS 163.095, or the charge name contains the words aggravated murder. "
        "Murder in the second degree, ORS 163.115, is not excluded."
    ),
    "sentence-completed": (
        "Asked of the client. OECI records no post-prison supervision or probation end date, "
        "and a case status of Closed describes the court case rather than supervision."
    ),
    "not-registerable-sex-offense": (
        "Fails where the statute section is one listed as a sex crime in ORS 163A.005(5)(a) to "
        "(y), or where the charge name records an attempt or conspiracy to commit one of them, "
        "per paragraphs (z) and (bb). Burglary with intent to commit one, paragraph (aa), cannot "
        "be detected, because OECI records the burglary statute without the intent. Asked of the "
        "client where the crime, or the crime attempted, requires reporting only in circumstances "
        "OECI does not record, such as the age of the victim or a court designation."
    ),
    "no-domestic-violence": (
        "Asked of the client. OECI does not record whether a conviction involved domestic " "violence."
    ),
    "substantial-rehabilitation": "Neither the record nor the client settles this. See section 5.4.",
    "manifest-hardship": "Neither the record nor the client settles this. See section 5.4.",
}

SCOPE_WORDING = {
    SB819Scope.CASE: "the case, and is answered once for that prosecution",
    SB819Scope.CHARGE: "this conviction",
}

PATHWAY_ORDER = [SB819Pathway.COLLATERAL_CONSEQUENCES]

SCOPE_KEYS = ["in-multnomah", "not-expungeable"]

SOURCE_URL = "https://www.mcda.us/wp-content/uploads/2021/11/SB-819-Application-Information-Sheet.pdf"


def _citation_url(citation: str) -> str:
    """Deep link to the page a criterion is drawn from.

    Most PDF viewers honour the #page fragment, and the ones that do not still open the
    document, so the link is never worse than the citation alone.
    """
    page = re.search(r"\d+", citation)
    return f"{SOURCE_URL}#page={page.group()}" if page else SOURCE_URL


RESOLUTION = [
    (
        "5.1",
        "Each criterion is Met, Not met, or Unresolved. It is settled once its source "
        "speaks: the record for those determined from OECI, the client for those put as a "
        "question. Until then it is Unresolved.",
    ),
    (
        "5.2",
        "A pathway is unavailable if any of its criteria is Not met; unresolved if none is "
        "Not met but any is Unresolved; and available only if all of them are Met.",
    ),
    (
        "5.3",
        "A conviction takes the result of its pathway, and is never better than its main "
        "criteria. A main criterion that is Not met ends the analysis, and the pathway is not "
        "considered.",
    ),
    (
        "5.4",
        "Two criteria are settled by neither the record nor the client: the showings of "
        "rehabilitation and of hardship that the applicant assembles afterwards. Counting them "
        "would hold the pathway unresolved permanently, so they take no part in 5.1 to 5.3. A "
        "conviction reported as possibly eligible has cleared every criterion the record and "
        "the client can settle, and nothing further.",
    ),
]


def all_criteria(module) -> List[SB819Criterion]:
    """Every criterion the module defines, in the order it defines them."""
    return [v for k, v in vars(module).items() if k.isupper() and isinstance(v, SB819Criterion)]


def collect_questions(analysis) -> Dict[str, SB819Question]:
    """The wording each criterion is put to the client with, taken from a real analysis."""
    found: Dict[str, SB819Question] = {}
    for charge in analysis.charge_analyses:
        results = list(charge.main_criterion_results)
        for pathway in charge.pathway_results:
            results += list(pathway.criterion_results)
        for result in results:
            if result.question and result.criterion.key not in found:
                found[result.criterion.key] = result.question
    return found


def _criterion_block(number: str, criterion: SB819Criterion, screened: bool = True) -> Dict:
    return {
        "kind": "criterion",
        "number": number,
        "key": criterion.key,
        "name": criterion.name,
        "citation": criterion.citation,
        "citation_url": _citation_url(criterion.citation),
        "source_text": criterion.description,
        "how_determined": HOW_DETERMINED[criterion.key],
        "concerns": SCOPE_WORDING[criterion.scope] if criterion.determination is SB819Determination.QUESTION else "",
        "screened": screened,
    }


def build(module, questions_by_key: Dict[str, SB819Question]) -> Dict:
    """The county's criteria as a numbered sheet, for a reader auditing the rules."""
    criteria = all_criteria(module)
    numbers: Dict[str, str] = {}
    sections: List[Dict] = []

    scope = [c for c in criteria if c.key in SCOPE_KEYS]
    blocks = []
    for i, criterion in enumerate(scope, start=1):
        numbers[criterion.key] = f"1.{i}"
        blocks.append(_criterion_block(f"1.{i}", criterion))
    sections.append(
        {
            "number": "1",
            "title": "Which convictions are screened",
            "rule": "Only convictions are considered, and traffic violations and parking tickets "
            "are left out as the search summary leaves them out. Two of the four main criteria on page 3 "
            "are applied as a filter rather than as a verdict. A conviction is screened if and "
            "only if 1.1 AND 1.2; one failing either is left out of the analysis rather than "
            "reported ineligible, since in the first case no criteria have been published for "
            "it, and in the second expungement remains the route open to it.",
            "blocks": blocks,
        }
    )

    main = [c for c in criteria if c.pathway is None and c.key not in SCOPE_KEYS]
    blocks = []
    for i, criterion in enumerate(main, start=1):
        numbers[criterion.key] = f"2.{i}"
        blocks.append(_criterion_block(f"2.{i}", criterion))
    sections.append(
        {
            "number": "2",
            "title": "Main criteria",
            "rule": "The remaining two main criteria from page 3, which gate every "
            "application type. A conviction passes if and only if "
            + " AND ".join(f"2.{i}" for i in range(1, len(main) + 1))
            + ". One failing either is reported ineligible, and no pathway is considered.",
            "blocks": blocks,
        }
    )

    sections.append(
        {
            "number": "3",
            "title": "Pathway",
            "rule": f"A conviction that passes section 2 is considered under the {PATHWAY_ORDER[0].value} "
            "application type, and takes the result of 3.1.",
            "blocks": [],
        }
    )

    for p_index, pathway in enumerate(PATHWAY_ORDER, start=1):
        members = [c for c in criteria if c.pathway is pathway]
        screened = [c for c in members if c.is_screenable]
        unscreened = [c for c in members if not c.is_screenable]

        clause = " AND ".join(f"3.{p_index}.{i}" for i in range(1, len(screened) + 1))

        blocks = []
        for i, criterion in enumerate(screened, start=1):
            numbers[criterion.key] = f"3.{p_index}.{i}"
            blocks.append(_criterion_block(f"3.{p_index}.{i}", criterion))

        for criterion in unscreened:
            numbers[criterion.key] = ""
            blocks.append(_criterion_block("", criterion, screened=False))

        rule = f"Available if and only if {clause}."
        gates = [c for c in screened if c.is_gate]
        if gates:
            rule += (
                f" {numbers[gates[0].key]} is put to the client first, and the pathway's other questions "
                "are asked only once it is met."
            )

        sections.append({"number": f"3.{p_index}", "title": pathway.value, "rule": rule, "blocks": blocks})

    questions = [
        {
            "number": numbers.get(criterion.key, ""),
            "name": criterion.name,
            "text": questions_by_key[criterion.key].text,
            "if_yes": questions_by_key[criterion.key].if_yes.value,
            "if_no": questions_by_key[criterion.key].if_no.value,
            "note": questions_by_key[criterion.key].note,
        }
        for criterion in criteria
        if criterion.key in questions_by_key
    ]

    return {
        "county": module.COUNTY,
        "source": "Multnomah County District Attorney, Justice Integrity Unit, SB 819 "
        "Application Information Sheet, version 2021.11.05. The page cite on each criterion "
        "links to the page it is drawn from, and the quoted text is that document's own wording.",
        "source_title": "SB 819 Application Information Sheet",
        "source_url": SOURCE_URL,
        "sections": sections,
        "questions": questions,
        "resolution": [{"number": n, "text": t} for n, t in RESOLUTION],
    }
