# SB-819 view, second implementation: the logic diagram with every string on screen

The same stages and states as [skeleton-and-logic.md](skeleton-and-logic.md), with the
text the screen shows at each point. Strings the payload supplies are marked `(payload)`
and given as the Multnomah ruleset emits them today; the view never rewrites them.

## Header (always)

```
+--------------------------------------------------------------------------+
| SB-819 Eligibility Analysis                     [<- Back to Search Summary]|
|--------------------------------------------------------------------------|
| Full rules                                                                |
+--------------------------------------------------------------------------+
```

- Heading: `SB-819 Eligibility Analysis`
- Button: `Back to Search Summary` (returns to the record summary and scrolls it to the top)
- Link: `Full rules` (opens `/sb819-rules` in a new tab)

## The badge, in the ordinary record summary

Beside the `Ineligible` group heading. One of:

- `Check SB-819 eligibility` (purple), when any analyzed charge is not Ineligible on the
  current answers
- `No charges SB-819 eligible` (red), otherwise

Accessible name: `<label>. Open the SB-819 eligibility analysis.` Absent when no charge is
in scope.

## Applicant panel (S0)

```
+--------------------------------------------------------------------------+
| About the applicant                                     1 of 1 answered  |
| |                                                                        |
| | Is the applicant currently incarcerated?                               |
| | ( ) Yes   (o) No   Clear                                               |
+--------------------------------------------------------------------------+
```

- Heading: `About the applicant`
- Count: `<answered> of <asked> answered`, over the Answered and Live record-scope questions
- Each question: its text `(payload)`, then `Yes`, `No`, and `Clear` once answered
- The panel is absent when no record-scope question is Answered or Live (every one waits on
  a main-criterion question on every charge)

Record-scope question texts `(payload)`:

| # | Text |
| --- | --- |
| Q3 | Is the applicant currently incarcerated? |
| Q7 | Was the applicant sentenced as a juvenile, with incarceration remaining, approaching age 25 and facing transfer to adult prison? |
| Q9 | Is the applicant over 60, terminally or debilitatingly ill, or currently on hospice care? |
| Q10 | Do the applicant's sentences for non-person crimes total more than 10 years? |
| Q11 | Do the applicant's sentences for person crimes total more than 16 years? |

Q7, Q9, Q10 and Q11 appear only after Q3 is answered Yes, and each disappears again once
another of them is answered Yes.

Below this panel, nothing renders while any Live record-scope question is unanswered.

## Summary (S1)

```
+--------------------------------------------------------------------------+
| Possibly SB-819 Eligible                                                 |
|   None                                                                   |
| Needs More Analysis (6)                                                  |
|   SB819-1000: Kidnapping in the First Degree                             |
|   ...                                                                    |
| SB-819 Ineligible (2)                                                    |
|   SB819-300: Driving Under the Influence of Intoxicants                  |
|   SB819-400: Aggravated Murder                                           |
+--------------------------------------------------------------------------+
```

- Section headings, in this order: `Possibly SB-819 Eligible`, `Needs More Analysis`,
  `SB-819 Ineligible`, each followed by `(<count>)` when the count is not zero
- Each charge: `<case number>: <charge name (payload)>`, linked to the case panel
- Empty section: `None`

## Case panel (S1)

```
+--------------------------------------------------------------------------+
| Case          County       Status      Balance                           |
| SB819-1000    Multnomah    Closed      $0.00                             |
|                                                                          |
| | Has the applicant fully completed the sentence on this case,           |
| | including all post-prison supervision and probation?                   |
| | ( ) Yes   ( ) No                                                       |
|                                                                          |
|   Charge   163235-Kidnapping in the First Degree                         |
+--------------------------------------------------------------------------+
```

- Labels: `Case` (the number, linked to the OECI case detail), `County`, `Status`, `Balance`
- The case's questions, in the same block style, when any is Answered or Live on the case

Case-scope question texts `(payload)`:

| # | Text |
| --- | --- |
| Q12 | Has the applicant fully completed the sentence on this case, including all post-prison supervision and probation? |
| Q5 | Was this conviction part of a global plea deal involving multiple counties? |

Q5 appears only after Q3 is answered Yes.

- Each charge on the case, while a case-scope question live on that charge is unanswered:
  one line, `Charge` and then `<statute>-<name>`

## Charge panel (S2)

```
+------------------------------------------------------------------------+
|  Charge        164405-Robbery in the Second Degree                     |
|  Severity      Felony Class B                                          |
|  Disposition   Convicted - Jan 1, 2010                                 |
|  Charged       Jan 1, 2010                                             |
|------------------------------------------------------------------------|
|  More Info  v                                                          |
|------------------------------------------------------------------------|
| | Is the applicant asserting that they are actually innocent of this   |
| | conviction?                                                           |
| | ( ) Yes   ( ) No                                                      |
| | Did this conviction involve domestic violence?                        |
| | ( ) Yes   ( ) No                                                      |
+------------------------------------------------------------------------+
```

- Labels: `Charge`, `Severity`, `Disposition`, `Charged`
- Disposition: `<status> - <date>` for Convicted or Dismissed; `<status> ("<ruling>")` for
  Unrecognized; otherwise the status
- `More Info`: the record view's expungement-rules disclosure, unchanged
- The charge's questions, in the block style, when any is Answered or Live on the charge

Charge-scope question texts `(payload)`:

| # | Text |
| --- | --- |
| Q1 | Was this conviction sentenced as a felony? |
| Q2 | Is the applicant asserting that they are actually innocent of this conviction? |
| Q4 | Has the applicant served at least five years of the term of incarceration on this sentence? |
| Q6 | Was this conviction sentenced under ORS 137.690 or ORS 137.719? |
| Q8 | Was the applicant under 18 when this crime was committed? |
| Q13 | Does this conviction require the applicant to report as a sex offender? |
| Q14 | Did this conviction involve domestic violence? |

Q4, Q6 and Q8 appear only after Q3 is answered Yes; Q13 and Q14 only after Q12 is answered
Yes on the case; all of them only after Q1, when present, is answered Yes. Q14's payload
note, that a domestic violence conviction committed as a juvenile without an intimate
partner is not disqualifying, is not shown; see the design note at the end.

Below the questions, nothing renders while any Live charge-scope question is unanswered.

## Criteria (S3)

```
|------------------------------------------------------------------------|
|  SB-819 Limiting Criteria                                              |
|                                                                        |
|  Main Criteria  -- all four met                                     v  |
|                                                                        |
|  Actual Innocence  [Needs More Analysis]                            >  |
|                                                                        |
|  Excessive Sentencing  [SB-819 Ineligible]                          >  |
|    Is the applicant currently incarcerated?  No                        |
|                                                                        |
|  Collateral Consequences  [Possibly SB-819 Eligible]                v  |
|    (x) Applicant has fully completed the sentence          Question    |
|    (v) Conviction is not a registerable sex offense        OECI        |
|    (v) Conviction did not involve domestic violence        Question    |
+------------------------------------------------------------------------+
```

- Heading: `SB-819 Limiting Criteria`
- When the main criteria failed, one sentence: `This conviction fails a criterion that
  gates every application type, so the Justice Integrity Unit cannot accept it under any
  pathway.`
- When some pathways are Ineligible and some are not: `Blocked under <pathways>, but still
  open under <pathways>.` (blocked list joined with `, `, open list joined with ` and `)
- Main criteria disclosure: `Main Criteria`, then either `— all four met` (green, and the
  disclosure starts closed) or the main status as a pill (starts open)
- Each pathway disclosure: the pathway name `(payload)` and its status as a pill
- Status pills: `Possibly SB-819 Eligible` (green), `Needs More Analysis` (purple),
  `SB-819 Ineligible` (red)
- An Ineligible pathway while closed: its bar on one line. For a question criterion, the
  question text `(payload)` and then `Yes` or `No` in red; for a record criterion, the
  record's explanation `(payload)`
- Each row: the outcome icon (check, cross, or question mark), the criterion name
  `(payload)`, and the determination tag `OECI` or `Question`

Criterion names `(payload)`, in the order the rows appear:

| Section | Name |
| --- | --- |
| Main | Conviction is from Multnomah County |
| Main | Conviction is not expungeable under ORS 137.225 |
| Main | Conviction was sentenced as a felony |
| Main | Conviction is not aggravated murder |
| Actual Innocence | Applicant asserts actual innocence of the conviction |
| Excessive Sentencing | Applicant has served at least 5 years of the term of incarceration |
| Excessive Sentencing | Conviction was not part of a global plea deal across counties |
| Excessive Sentencing | Conviction is not subject to ORS 137.690 or ORS 137.719 |
| Excessive Sentencing | Applicant committed the crime when under 18 |
| Collateral Consequences | Applicant has fully completed the sentence |
| Collateral Consequences | Conviction is not a registerable sex offense |
| Collateral Consequences | Conviction did not involve domestic violence |

Not rows: the record-scope criteria (`Applicant is currently incarcerated`, `Sentenced as
a juvenile and approaching transfer to adult prison`, `Applicant is over 60, terminally or
debilitatingly ill, or on hospice care`, `Non-person crime with sentences longer than 10
years in total`, `Person crime with sentences longer than 16 years in total`), which are
answered once at the top; and the three nobody can settle (`The JIU can identify an avenue
of investigation`, `Applicant demonstrates substantial rehabilitation and low risk`,
`Applicant demonstrates manifest and particularized hardship`). A row whose question is
Dormant is also omitted.

Record explanations that can appear as a pathway's bar `(payload)`:

| Criterion | Explanation |
| --- | --- |
| Conviction is not a registerable sex offense | This conviction is a registerable sex offense under ORS 163A.005. |
| Applicant committed the crime when under 18 | The applicant was about `<age>` at the time of this offense. |
| Non-person crime with sentences longer than 10 years in total | This conviction is for a person crime, so the non-person threshold does not apply. |
| Person crime with sentences longer than 16 years in total | This conviction is for a non-person crime, so the person threshold does not apply. |

The last three bar the pathway only together with every other alternative, since they are
members of the disjunction group.

## The state diagram, annotated

```
S0 ──[Q3 answered; Q7/Q9/Q10/Q11 answered if Live]──> S1
S1 ──[per case: Q12 answered; Q5 answered if Live]────> S2 for that case's charges
S2 ──[per charge: Q1, Q2, Q4, Q6, Q8, Q13, Q14 answered, those that are Live]──> S3

At every stage an answer anywhere re-runs resolution and every stage predicate:
  a Yes on a gate can move a charge from S3 back to S2 (a new question is Live),
  a No on a gate can move it from S2 to S3 (its remaining questions went Dormant),
  Clear on any answer restores whatever that answer had made Dormant.
```

## Design notes carried into the implementation

- The domestic violence exception in the payload note is not on screen, because the
  questions carry only their text. Folding the exception into the question text belongs in
  the ruleset, where the wording is owned.
- The applicant panel is not collapsible. It holds at most five short questions.
- Disclosures are the app's `useDisclosure` hook with the `hidden` attribute; there is no
  height animation and no selectable-header workaround.
