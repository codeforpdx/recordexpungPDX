"""Multnomah County's published SB-819 limiting criteria.

Source: Multnomah County District Attorney, Justice Integrity Unit, "SB 819 Application
Information Sheet", version 2021.11.05. Page cites on each criterion refer to it.

RecordSponge screens the Collateral Consequences application type. Four main criteria gate
it; the pathway then adds its own. A charge is analyzed only if it is a Multnomah conviction
that RecordSponge found ineligible under ORS 137.225, so both of those main criteria always
pass here and are reported for transparency.
"""

from typing import List

from expungeservice.models.sb819 import (
    SB819Criterion,
    SB819Scope,
    SB819CriterionResult,
    SB819Determination,
    SB819Outcome,
    SB819Pathway,
    SB819Question,
    SB819Ruleset,
    SB819Status,
)
from expungeservice.sb819_criteria.registerable_sex_offenses import (
    is_conditionally_registerable,
    is_registerable_sex_offense,
)

COUNTY = "Multnomah"

AGGRAVATED_MURDER_STATUTE = "163095"


# ---------------------------------------------------------------------------
# Criteria
# ---------------------------------------------------------------------------

IN_MULTNOMAH = SB819Criterion(
    key="in-multnomah",
    name="Conviction is from Multnomah County",
    description="The JIU can only accept applicants whose convictions are from Multnomah County.",
    citation="Pages 1, 3",
    determination=SB819Determination.OECI,
)

NOT_EXPUNGEABLE = SB819Criterion(
    key="not-expungeable",
    name="Conviction is not expungeable under ORS 137.225",
    description=(
        "SB 819 relief applies to convictions that are not eligible for expungement. "
        "If the record can be expunged, that is the required route instead."
    ),
    citation="Page 3",
    determination=SB819Determination.OECI,
)

SENTENCED_AS_FELONY = SB819Criterion(
    key="sentenced-as-felony",
    name="Conviction was sentenced as a felony",
    description="Only convictions sentenced as felonies qualify. Misdemeanor-sentenced convictions are ineligible.",
    citation="Page 3",
    determination=SB819Determination.OECI,
)

NOT_AGGRAVATED_MURDER = SB819Criterion(
    key="not-aggravated-murder",
    name="Conviction is not aggravated murder",
    description="Aggravated murder convictions are categorically excluded from SB 819 relief.",
    citation="Page 3",
    determination=SB819Determination.OECI,
)

SENTENCE_COMPLETED = SB819Criterion(
    key="sentence-completed",
    scope=SB819Scope.CASE,
    name="Applicant has fully completed the sentence",
    description=(
        "The applicant must have fully completed their sentence, including all post-prison "
        "supervision or probation, before applying under this pathway."
    ),
    citation="Page 4",
    determination=SB819Determination.QUESTION,
    pathway=SB819Pathway.COLLATERAL_CONSEQUENCES,
    is_gate=True,
)

NOT_REGISTERABLE_SEX_OFFENSE = SB819Criterion(
    key="not-registerable-sex-offense",
    name="Conviction is not a registerable sex offense",
    description="Registerable sex offenses are excluded from the collateral consequences pathway.",
    citation="Page 5",
    determination=SB819Determination.OECI,
    pathway=SB819Pathway.COLLATERAL_CONSEQUENCES,
)

NO_DOMESTIC_VIOLENCE = SB819Criterion(
    key="no-domestic-violence",
    name="Conviction did not involve domestic violence",
    description=(
        "A domestic violence conviction is not disqualifying if it was committed while the "
        "applicant was a juvenile and did not involve an intimate partner."
    ),
    citation="Page 5",
    determination=SB819Determination.QUESTION,
    pathway=SB819Pathway.COLLATERAL_CONSEQUENCES,
)

SUBSTANTIAL_REHABILITATION = SB819Criterion(
    key="substantial-rehabilitation",
    name="Applicant demonstrates substantial rehabilitation and low risk",
    description=(
        "The applicant must demonstrate substantial rehabilitation and present as low risk for "
        "further criminality. Factors include treatment, payment of financial obligations, compliance "
        "with court conditions, pro-social involvement, stable employment, academic or professional "
        "accomplishments, and no subsequent convictions."
    ),
    citation="Page 5",
    determination=SB819Determination.PART_TWO,
    pathway=SB819Pathway.COLLATERAL_CONSEQUENCES,
)

MANIFEST_HARDSHIP = SB819Criterion(
    key="manifest-hardship",
    name="Applicant demonstrates manifest and particularized hardship",
    description=(
        "The applicant must show a consequence of the conviction more severe than a typical similarly "
        "situated individual, such as housing, professional licensure, continued employment, or access "
        "to necessary medical treatment or therapy."
    ),
    citation="Page 5",
    determination=SB819Determination.PART_TWO,
    pathway=SB819Pathway.COLLATERAL_CONSEQUENCES,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_felony_level(level: str) -> bool:
    # "Felony Unclassified" counts; the JIU criterion turns on felony sentencing, not class.
    return "felony" in level.lower()


def _sentencing_level_is_uncertain(charge) -> bool:
    """True when the level OECI records may not be the level the charge was sentenced at."""
    return (
        charge.disposition.lesser_charge
        or charge.disposition.amended
        or "reduced to violation" in charge.charge_type.type_name.lower()
    )


def _is_aggravated_murder(charge) -> bool:
    # Narrower than the SevereCharge charge type, which name-matches all murder. SB 819
    # excludes aggravated murder (ORS 163.095) only; Murder II (ORS 163.115) is not excluded.
    return charge.statute.upper().startswith(AGGRAVATED_MURDER_STATUTE) or "aggravated murder" in charge.name.lower()


# ---------------------------------------------------------------------------
# Main criteria
# ---------------------------------------------------------------------------


def main_criteria(charge, case, record) -> List[SB819CriterionResult]:
    return [
        _in_multnomah(case),
        _not_expungeable(charge),
        _sentenced_as_felony(charge),
        _not_aggravated_murder(charge),
    ]


def _in_multnomah(case) -> SB819CriterionResult:
    return SB819CriterionResult(
        criterion=IN_MULTNOMAH,
        outcome=SB819Outcome.PASSED,
        explanation=f"The conviction is from {case.summary.location} County.",
    )


def _not_expungeable(charge) -> SB819CriterionResult:
    return SB819CriterionResult(
        criterion=NOT_EXPUNGEABLE,
        outcome=SB819Outcome.PASSED,
        explanation="RecordSponge found this conviction ineligible for expungement under ORS 137.225.",
    )


def _sentenced_as_felony(charge) -> SB819CriterionResult:
    if not _is_felony_level(charge.level):
        return SB819CriterionResult(
            criterion=SENTENCED_AS_FELONY,
            outcome=SB819Outcome.FAILED,
            explanation=f'This conviction is recorded at the level "{charge.level}", which is not a felony.',
        )
    if _sentencing_level_is_uncertain(charge):
        return SB819CriterionResult(
            criterion=SENTENCED_AS_FELONY,
            outcome=SB819Outcome.UNKNOWN,
            explanation=(
                f'This conviction is charged at "{charge.level}", but the disposition indicates the charge was '
                "reduced or amended, so the level it was sentenced at may be lower."
            ),
            question=SB819Question(
                text="Was this conviction sentenced as a felony?",
                if_yes=SB819Status.POSSIBLY_ELIGIBLE,
                if_no=SB819Status.INELIGIBLE,
            ),
        )
    return SB819CriterionResult(
        criterion=SENTENCED_AS_FELONY,
        outcome=SB819Outcome.PASSED,
        explanation=f'This conviction was sentenced as a felony ("{charge.level}").',
    )


def _not_aggravated_murder(charge) -> SB819CriterionResult:
    if _is_aggravated_murder(charge):
        return SB819CriterionResult(
            criterion=NOT_AGGRAVATED_MURDER,
            outcome=SB819Outcome.FAILED,
            explanation="This conviction is for aggravated murder, which SB 819 excludes categorically.",
        )
    return SB819CriterionResult(
        criterion=NOT_AGGRAVATED_MURDER,
        outcome=SB819Outcome.PASSED,
        explanation="This conviction is not for aggravated murder.",
    )


# ---------------------------------------------------------------------------
# Pathway: Collateral Consequences
# ---------------------------------------------------------------------------


def collateral_consequences(charge, case, record) -> List[SB819CriterionResult]:
    return [
        _sentence_completed(),
        _not_registerable_sex_offense(charge),
        _no_domestic_violence(),
        SB819CriterionResult(
            criterion=SUBSTANTIAL_REHABILITATION,
            outcome=SB819Outcome.UNKNOWN,
            explanation="Assessed from the applicant's own materials, outside this analysis.",
        ),
        SB819CriterionResult(
            criterion=MANIFEST_HARDSHIP,
            outcome=SB819Outcome.UNKNOWN,
            explanation="Assessed from the applicant's own materials, outside this analysis.",
        ),
    ]


def _sentence_completed() -> SB819CriterionResult:
    return SB819CriterionResult(
        criterion=SENTENCE_COMPLETED,
        outcome=SB819Outcome.UNKNOWN,
        explanation=(
            "OECI does not record post-prison supervision or probation end dates. A case status of "
            "Closed describes the court case, not supervision."
        ),
        question=SB819Question(
            text=(
                "Has the applicant fully completed the sentence on this case, including all post-prison "
                "supervision and probation?"
            ),
            if_yes=SB819Status.POSSIBLY_ELIGIBLE,
            if_no=SB819Status.INELIGIBLE,
        ),
    )


def _not_registerable_sex_offense(charge) -> SB819CriterionResult:
    if is_registerable_sex_offense(charge.statute, charge.name):
        if is_conditionally_registerable(charge.statute, charge.name):
            return SB819CriterionResult(
                criterion=NOT_REGISTERABLE_SEX_OFFENSE,
                outcome=SB819Outcome.UNKNOWN,
                explanation=(
                    "This offense requires sex offender reporting only in circumstances OECI does not "
                    "record, such as the age of the victim or a court designation."
                ),
                question=SB819Question(
                    text="Does this conviction require the applicant to report as a sex offender?",
                    if_yes=SB819Status.INELIGIBLE,
                    if_no=SB819Status.POSSIBLY_ELIGIBLE,
                ),
            )
        return SB819CriterionResult(
            criterion=NOT_REGISTERABLE_SEX_OFFENSE,
            outcome=SB819Outcome.FAILED,
            explanation="This conviction is a registerable sex offense under ORS 163A.005.",
        )
    return SB819CriterionResult(
        criterion=NOT_REGISTERABLE_SEX_OFFENSE,
        outcome=SB819Outcome.PASSED,
        explanation="This conviction is not a registerable sex offense under ORS 163A.005.",
    )


def _no_domestic_violence() -> SB819CriterionResult:
    return SB819CriterionResult(
        criterion=NO_DOMESTIC_VIOLENCE,
        outcome=SB819Outcome.UNKNOWN,
        explanation="OECI does not record whether a conviction involved domestic violence.",
        question=SB819Question(
            text="Did this conviction involve domestic violence?",
            if_yes=SB819Status.INELIGIBLE,
            if_no=SB819Status.POSSIBLY_ELIGIBLE,
            note=(
                "A domestic violence conviction is not disqualifying if it was committed while the applicant "
                "was a juvenile and did not involve an intimate partner."
            ),
        ),
    )


RULESET = SB819Ruleset(
    county=COUNTY,
    main_criteria=main_criteria,
    pathways={SB819Pathway.COLLATERAL_CONSEQUENCES: collateral_consequences},
)
