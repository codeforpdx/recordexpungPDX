# SB-819 view, second implementation: skeleton and state logic

The view screens the convictions RecordSponge finds ineligible for expungement against
Multnomah County's published SB-819 limiting criteria, and lets a volunteer answer the
questions the record cannot settle. This file states what the view is made of and the rules
that decide what is on screen at any moment. Every rule here is a pure function of two
inputs: the analysis in the search payload and the answers given so far.

Sources: the DA's [SB 819 Application Information Sheet](../SB-819-Application-Information-Sheet.pdf)
(version 2021.11.05, pages 3 to 5), `expungeservice/models/sb819.py`,
`expungeservice/sb819_criteria/multnomah.py`, `expungeservice/serializer.py`, and
`src/shared/sb819ResolutionFixtures.json`.

## 1. Inputs

**The analysis.** For every conviction in scope (a Multnomah conviction that RecordSponge
found ineligible under ORS 137.225, excluding the traffic and parking charge types the
summary hides), the payload carries four main criteria and three pathways, each pathway a
list of criteria. A criterion carries:

| Field | Meaning |
| --- | --- |
| `key` | Stable identifier; answers key off it |
| `scope` | `record`, `case`, or `charge`: what the criterion is a fact about, so how often it is asked |
| `pathway` | One of the three, or `null` for a main criterion |
| `determination` | `OECI` (the record settles it), `Question` (the client settles it), `Discretion` or `Part 2` (settled later, by the DA or by documents) |
| `is_screenable` | `OECI` or `Question`. Only these take part in any status |
| `disjunction_group` | Members of a group satisfy the pathway if any one passes |
| `is_gate` | The one question that defines who a pathway is for |
| `outcome` | `Passed`, `Failed`, or `Unknown`, as the record left it |
| `question` | For an `Unknown` criterion the client can settle: text, `if_yes`, `if_no`, note |

**The answers.** A map from target to `yes` or `no`. A target names one question at its
scope: `record:<key>`, `case:<case number>:<key>`, or `charge:<charge id>:<key>`. One
record-scope answer reaches every charge; one case-scope answer reaches every charge on
that case.

Answers live in the Redux store for the session only, cleared by a new search and by Start
Over, kept across an edit to the current record.

## 2. Resolution

Resolution turns the analysis plus the answers into a status for every pathway and every
charge. It is the algebra pinned by the shared fixture table, restated here because the
view's every decision rests on it.

1. **Answer to outcome.** An `Unknown` criterion with a question takes `if_yes` or `if_no`
   according to the answer. A resulting status of Ineligible is `Failed`; anything else is
   `Passed`. Unanswered stays `Unknown`. A criterion that is not screenable is never
   touched.
2. **Groups.** A disjunction group is `Passed` if any member passed, else `Unknown` if any
   member is unknown, else `Failed`.
3. **Pathway status.** Over the screenable criteria, with each group counted once: any
   `Failed` gives Ineligible; else any `Unknown` gives Needs More Analysis; else Possibly
   Eligible.
4. **Charge status.** A failed main criterion gives Ineligible and empties the pathways.
   Otherwise the charge is the worse of its main status and its best pathway status.
5. **Sections.** The three sections list the charges by status, in the order Possibly
   Eligible, Needs More Analysis, Ineligible.
6. **What barred a pathway.** The failed criteria not in a group, plus the members of any
   group whose every member failed, in evaluation order. A single failed alternative is
   never a bar.

## 3. Question state

Every question in the analysis is in exactly one of three states, recomputed from the
resolved analysis on every answer.

| State | Definition | Shown |
| --- | --- | --- |
| **Answered** | An answer is stored for its target | Always, with the answer selected and a Clear control |
| **Live** | Unanswered, and answering it now could change a status somewhere | Yes |
| **Dormant** | Unanswered, and nothing turns on it yet or any more | No |

A question is Live if it is live on at least one charge it serves. It is live on a charge
when all of the following hold on the resolved analysis of that charge:

- Its criterion's outcome on that charge is `Unknown`.
- The charge's main criteria have not failed.
- If it is a pathway criterion: the pathway is not Ineligible on that charge.
- If it is a pathway criterion: no main-criterion question on that charge is unanswered.
  A conviction that was not sentenced as a felony is out under every pathway, so that
  question comes first.
- If it is a pathway criterion and not the gate: the pathway's gate has `Passed`.
- If it is in a disjunction group: no member of the group has `Passed`. One met
  alternative satisfies the group, so the others are not asked.

An answered question is never Dormant. It is the record of a decision and the only way back
from it, so it stays on screen wherever it was asked, however much its answer has made
irrelevant.

There is no fourth state. A question the earlier implementation held behind a note, or set
aside behind a disclosure, is Dormant here and simply not rendered. Nothing is stranded:
every Dormant question is unanswered, and the answer that made it Dormant is itself
Answered and changeable.

## 4. Stages

The view reads top down in the order the answers are needed. Each level renders its own
questions and withholds everything beneath it until none of those questions is Live and
unanswered.

```
Header                       always
Applicant panel              record-scope questions (Answered + Live)
  |
  |  every Live record-scope question answered
  v
Summary                      three sections, re-bucketed on every answer
Case (each)
  Case questions             case-scope questions live on this case (Answered + Live)
  Charge (each)
    name line only           while a case-scope question live on THIS charge is unanswered
    otherwise:
    detail lines             charge, severity, disposition, date; expungement rules
    Charge questions         charge-scope questions (Answered + Live)
      |
      |  every Live charge-scope question answered
      v
    Criteria                 main criteria, then the three pathways
```

Two consequences follow and are intended:

- A charge the record rules out on the main criteria has no live question at any scope, so
  it renders its detail lines and its criteria at once, whatever is open on its case.
- An answer that unlocks a new question re-applies the stage rule. Answering "currently
  incarcerated" Yes brings up the alternatives, and the summary and cases wait until they
  are answered. Answering it Yes after a charge's criteria were shown brings up "five years
  served" on the charge, and that charge's criteria wait until it is answered.

## 5. Criteria

Rendered for a charge once its stage rule allows. Every row is the outcome icon, the
criterion's name, and how it is determined; nothing else. Questions were asked above, and a
ruled-out pathway names what ruled it out.

**Main criteria.** A disclosure headed "Main Criteria". When all four passed it reads "all
four met" beside the heading and starts closed. Otherwise it carries the main status as a
pill and starts open. Below it, when the main criteria failed, one sentence says that no
pathway can help.

**Pathways.** One disclosure per pathway, headed by its name and its status pill. It starts
open unless it is Ineligible or it is Actual Innocence. An Ineligible pathway, while closed,
shows one line naming what barred it: for a question, the question and the answer given;
for a record criterion, the record's explanation. When a pathway is Ineligible and another
is not, one sentence above the pathways says which are blocked and which are open.

**Rows in a pathway.** Its screenable criteria that are not record-scope, minus the rows of
Dormant questions. Record-scope criteria are answered once at the top and are not repeated
on every charge; Discretion and Part 2 criteria are not rows.

## 6. Summary and badge

The summary lists every analyzed conviction under its current status, "case number:
charge name", each linked to its case. Empty sections say "None".

The badge sits beside the Ineligible heading of the ordinary record summary. It reads
"Check SB-819 eligibility" when any analyzed charge is not Ineligible on the current
answers, "No charges SB-819 eligible" otherwise, and opens the view either way. It is
absent when no charge is in scope. Both the badge and the view render only on localhost
and the staging host, or under the build-time override.

## 7. Modules

All new code lives in `src/frontend/src/components/RecordSearch/SB819v2/`. It shares with
the rest of the app only the answers slice and the view-mode slice in `redux/`, the feature
flag, the `useDisclosure` hook, `DisclosureIcon`, and the record view's `ExpungementRules`.

| Module | Responsibility |
| --- | --- |
| `types.ts` | The payload shape, the answer map, the target function |
| `resolve.ts` | Section 2, pure |
| `questions.ts` | Section 3 and the stage predicates of section 4, pure |
| `useAnalysis.ts` | The resolved analysis for the current record and answers |
| `SB819View.tsx` | Section 4, top level |
| `Header.tsx`, `ApplicantPanel.tsx`, `Summary.tsx`, `CasePanel.tsx`, `ChargePanel.tsx`, `Criteria.tsx` | One stage each |
| `QuestionBlock.tsx`, `Question.tsx` | A block of questions in RecordSponge's own question style |
| `Badge.tsx` | Section 6 |
| `resolve.test.ts` | Executes the shared fixture table |
| `questions.test.ts` | Section 3 against small analyses |
| `SB819View.test.tsx` | A walk through the stages on the demo-shaped fixture |

## 8. The complete question and state diagram

### 8.1 The fourteen questions

The key, the scope, the pathway, and when the record puts the question at all. `Y` and `N`
give the status the answer resolves to: `P` Possibly Eligible, `I` Ineligible.

| # | Key | Scope | Pathway | Gate | Group | Y | N | Asked when |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | `sentenced-as-felony` | charge | main | | | P | I | Felony-level charge whose disposition is amended, a lesser charge, or reduced to a violation |
| Q2 | `innocence-claim` | charge | Actual Innocence | | | P | I | Always |
| Q3 | `currently-incarcerated` | record | Excessive Sentencing | gate | | P | I | Always |
| Q4 | `five-years-served` | charge | Excessive Sentencing | | | P | I | Always |
| Q5 | `not-global-plea` | case | Excessive Sentencing | | | I | P | Always |
| Q6 | `not-repeat-sex-offender` | charge | Excessive Sentencing | | | I | P | The record carries a felony sex crime conviction |
| Q7 | `juvenile-transfer` | record | Excessive Sentencing | | alternatives | P | I | Always |
| Q8 | `under-18-at-offense` | charge | Excessive Sentencing | | alternatives | P | I | No birth year, or the applicant turned 18 in the year of the offense |
| Q9 | `over-60-or-ill` | record | Excessive Sentencing | | alternatives | P | I | The applicant is not clearly over 60 |
| Q10 | `non-person-over-10-years` | record | Excessive Sentencing | | alternatives | P | I | The conviction is a non-person crime |
| Q11 | `person-over-16-years` | record | Excessive Sentencing | | alternatives | P | I | The conviction is a person crime |
| Q12 | `sentence-completed` | case | Collateral Consequences | gate | | P | I | Always |
| Q13 | `not-registerable-sex-offense` | charge | Collateral Consequences | | | I | P | The statute is registerable only in circumstances the record does not carry |
| Q14 | `no-domestic-violence` | charge | Collateral Consequences | | | I | P | Always |

Q10 and Q11 are record-scope with a charge-dependent outcome: on a person-crime charge Q10
is `Failed` from the record and only Q11 is a question, and the reverse on a non-person
charge. One answer to each still serves every charge it is a question on.

The six criteria that are never questions: `in-multnomah` and `not-expungeable` (always
passed, reported for completeness), `not-aggravated-murder` (record), `investigation-avenue`
(Discretion), `substantial-rehabilitation` and `manifest-hardship` (Part 2).

### 8.2 What each question waits on

```
                     +-----------------------------------------+
                     |  Q1  sentenced as a felony?  (per charge)|
                     |  present only on an amended disposition |
                     +-------------------+---------------------+
                                         | while unanswered, holds every
                                         | pathway question on its charge
        +--------------------------------+---------------------------------+
        |                                |                                 |
        v                                v                                 v
+---------------+   +-----------------------------------+   +---------------------------+
| Q2 innocence  |   | Q3 currently incarcerated? (record)|   | Q12 sentence completed?   |
| claim         |   |         gate, Excessive            |   | (per case) gate, Collateral|
| (per charge)  |   +-----------------+-----------------+   +-------------+-------------+
| no gate       |                     | Yes                               | Yes
+---------------+                     v                                   v
                  +-----------------------------------------+   +----------------------+
                  | Q4  five years served?     (per charge) |   | Q13 registerable?    |
                  | Q5  global plea deal?      (per case)   |   |     (per charge)     |
                  | Q6  ORS 137.690/137.719?   (per charge) |   | Q14 domestic violence|
                  +-----------------------------------------+   |     (per charge)     |
                  | alternatives, any one suffices:         |   +----------------------+
                  | Q7  juvenile transfer      (record)     |
                  | Q8  under 18 at offense    (per charge) |
                  | Q9  over 60 or ill         (record)     |
                  | Q10 non-person > 10 years  (record)     |
                  | Q11 person > 16 years      (record)     |
                  +-----------------------------------------+
                    once any alternative is met, the others
                    are Dormant
```

### 8.3 The state of one question

```
                     unanswered
                         |
        +----------------+-----------------+
        |                                  |
   live on some charge              live on no charge
        |                                  |
        v                                  v
      LIVE  ------ answer given ------>  ANSWERED  <---- answer given ------ DORMANT
        ^                                  |                                   ^
        |                                  | Clear                             |
        +----------------------------------+-----------------------------------+
                        (re-evaluated: live on some charge, or not)
```

"Live on a charge" is the conjunction in section 3. Every transition is a re-evaluation of
that predicate after an answer anywhere changes; there is no stored state beyond the answers.

### 8.4 The stages

```
S0  view opened
    Header. Applicant panel with Q3 alone; Q7, Q9, Q10 and Q11 wait on it.
    Nothing else.
        |
        | Q3 = No .............. Excessive Ineligible everywhere; Q4..Q11 Dormant
        | Q3 = Yes ............. Q7, Q9, Q10, Q11 Live as the record allows; wait for them
        |                        (each Yes among them makes the rest Dormant)
        v
S1  every Live record question answered
    Summary. Every case:
      case questions Live on the case: Q12 (always), Q5 (if Q3 = Yes)
      each charge: name line while a case question live on it is unanswered
        |
        | Q12 = No ............. Collateral Ineligible on the case; Q13, Q14 Dormant there
        | Q12 = Yes ............ Q13 (if present), Q14 Live on each charge
        | Q5  = Yes ............ Excessive Ineligible on the case; Q4, Q6, Q8 Dormant there
        v
S2  every Live case question on the charge answered
    Charge detail lines. Charge questions Live on it: Q1, Q2, Q4, Q6, Q8, Q13, Q14 as present
        |
        | Q1 = No .............. main Ineligible; every pathway question on the charge Dormant
        v
S3  every Live charge question answered
    Criteria: Main Criteria (pill or "all four met"), Actual Innocence (closed), Excessive
    Sentencing, Collateral Consequences (each open unless Ineligible, then closed behind
    its reason).
```

A charge the record rules out has no Live question at any scope and reaches S3 at once.

### 8.5 Statuses reachable per pathway on the demo record, with every question answered

| Pathway | Possibly Eligible | Needs More Analysis | Ineligible |
| --- | --- | --- | --- |
| Actual Innocence | Q2 = Yes | never once Q2 is answered | Q2 = No |
| Excessive Sentencing | Q3 = Yes, Q4 = Yes, Q5 = No, Q6 clear, one alternative met | while any of those is unanswered | Q3 = No, or Q4 = No, or Q5 = Yes, or Q6 = Yes, or every alternative failed |
| Collateral Consequences | Q12 = Yes, registerable clear, Q14 = No | while Q12, Q13, or Q14 is unanswered | Q12 = No, or registerable, or Q14 = Yes |

The charge takes the best of the three, never better than its main criteria.
