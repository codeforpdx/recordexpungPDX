# SB-819 view: the two implementations compared

The first implementation is `src/frontend/src/components/RecordSearch/SB819/`, as it
stands at commit `f6caba2c` on `jw/sb819-polish-pass-1`, after the polish pass of 30
September 2026. The second is `src/frontend/src/components/RecordSearch/SB819v2/`,
written from the design in [skeleton-and-logic.md](skeleton-and-logic.md) and
[logic-with-text.md](logic-with-text.md) without reading the first while writing. Both
render the same payload and share the same two Redux slices, the feature flag, the
disclosure hook, and the record view's expungement-rules component. The second is not
wired into the app; switching would be a one-line change in `Layout/index.tsx` and one in
`RecordSummary/ChargesList.tsx`.

## 1. Shape

| | First | Second |
| --- | --- | --- |
| Files | 23 | 19 |
| Lines, excluding tests and fixtures | 1,567 | 1,123 |
| Lines of tests and fixtures | 1,557 | 1,419 |
| Pure modules | `resolveAnalysis.ts`, `questionCollection.ts`, `types.ts` | `resolve.ts`, `questions.ts`, `types.ts` |
| Components | 14 | 10 |
| Test suites | 2 | 3 |

The second has no `SB819Held`, `SB819SetAside`, `SB819Collapse`, or
`useSelectableDisclosure`, and folds `SB819CaseQuestions` into `CasePanel`. The first
grew its shape by accretion over one afternoon and still carries the outline of features it
no longer has.

## 2. The state model

This is the substantive difference. Everything else follows from it.

**First.** `questionCollection.ts` partitions a panel's questions into `asked`, `setAside`,
and (implicitly, by exclusion) held. A question is held when, on every charge it serves, an
upstream question has not let it through; it is moot when its pathway is Ineligible on every
charge it serves; it is set aside when moot, not held, and unanswered; it is asked
otherwise, or whenever it is answered. Set-aside questions render folded behind a
disclosure that reads "N more questions, not needed because X is ruled out".

**Second.** `questions.ts` gives every question one of three states: answered, live, or
dormant. A question is live when, on some charge it serves, answering it could still change
a status. That predicate (`liveOnCharge`) is one conjunction: the criterion is still
unknown there; the charge's main criteria have not failed; no main-criterion question on
the charge is open; the pathway is not ruled out; the pathway's gate has passed; and no
alternative in the question's group has already passed. Dormant questions are not rendered
at all; there is no set-aside disclosure.

Three behaviors differ as a result.

| Situation | First | Second |
| --- | --- | --- |
| One alternative in the sentencing group is met, say juvenile transfer Yes | The other alternatives stay on the applicant panel and keep counting as unanswered | The others go dormant. One met alternative satisfies the group, so nothing turns on them |
| A pathway is ruled out by an answer other than its gate, say five years served No | Its unanswered questions fold into a "not needed" disclosure with a Show toggle | They are dormant and gone. The answer that ruled the pathway out is on screen and changeable |
| The main criteria failed by the record | Handled by a special case in `SB819Case` (`ruledOutByTheRecord`) so the charge is not held by its case's question | Falls out of the rule: no question is live on such a charge, so nothing holds it |

The first two are improvements the first implementation should take. The third is the
same behavior reached by a general rule instead of an exception.

## 3. What a case question holds

**First.** A case's charges are all listed by name while any question in the case's panel
is unanswered, with the record-ruled-out exception above.

**Second.** Each charge is held by name only while a case question that is live *on that
charge* is unanswered. On a case with one conviction whose Collateral Consequences is out
from the record (a registerable offense) and another whose is not, the first shows in full
at once while the second waits for the sentence-completion answer. In the first
implementation both wait.

## 4. Criteria rows

Both show every row as the outcome icon, the name, and the determination tag, and neither
repeats a record-scope criterion on a charge.

**First.** A pathway row is omitted only when its gate was answered against the pathway. A
question left unknown for any other reason still appears with a question-mark icon: five
years served when the plea answer ruled the pathway out, under 18 when time served did.

**Second.** Every unknown-question row is omitted. By the time the criteria are shown,
every live question on the charge is answered, so an unknown question left in a pathway is
dormant by construction. The rule is one filter (`pathwayRows`) instead of a per-row call
into the holding logic.

The second is right and the first should adopt it.

## 5. Panels and chrome

| | First | Second |
| --- | --- | --- |
| Applicant panel | Collapsible; reads "N of M answered" or "N not needed" | Not collapsible; reads "N of M answered" |
| Disclosures | Animated height; header text selectable without toggling | The hook's `hidden` attribute, no animation |
| Stage rule at the top | Summary and cases wait on every asked applicant question | Same |
| Header, summary, badge, charge detail lines | Same text and structure | Same |
| Empty question blocks | Guarded | Guarded (added on review; the first draft rendered an empty bordered wrapper) |

The animation and the selectable header are the first implementation's genuine extras and
worth keeping. The "N not needed" reading disappears with the set-aside disclosure.

## 6. Resolution

Identical algebra; both execute the shared fixture table. The second runs each scenario
through the top-level `resolveAnalysis` as a one-charge analysis, so the function the view
calls is under test, and adds one scenario asserting the sections and the badge flag are
recomputed. The first tests the four pieces separately and never calls the top-level
function from the fixture suite.

## 7. Tests

**First.** 53 view tests in one file, organized by the history of the afternoon: several
describe blocks were rewritten as the flow changed, helpers like `reachTheReasoning` and
`meetTheGate` encode a path through the stages, and a few tests assert what the code did
rather than what the design says.

**Second.** 14 state tests against the pure model (`questions.test.ts`), 21 view tests
organized by stage (`SB819View.test.tsx`), and the 16 fixture scenarios. Writing them
against the design first caught six wrong expectations in my own tests and no defect in
the model, which is what a state model with a unit suite is for.

The first implementation has no direct test of its question partition.

## 8. Findings to carry into the first implementation

In order of value:

1. **Adopt the three-state model.** Replace the asked/held/set-aside partition with
   answered/live/dormant and the `liveOnCharge` predicate. This delivers the group-met
   rule, drops the set-aside disclosure and `SB819SetAside`, and removes the "N not
   needed" reading.
2. **Hold a charge per charge.** A conviction is listed by name only while a case question
   live on that conviction is unanswered. This retires `ruledOutByTheRecord`.
3. **Omit every unknown-question row from the criteria.** One filter in place of the
   per-row holding check.
4. **Run the fixture table through `resolveAnalysis`**, and assert the sections and the
   badge flag.
5. **Add a state suite** for the question model.

Not carried: the plain disclosures and the non-collapsible applicant panel. The first
implementation's animation, selectable headers, and collapsible panel stay.

## 9. What to do with the second implementation

Once the first absorbs the findings above, the two differ only in chrome, and the second
can be deleted. Until then it is the reference for the state model, and its state suite is
the specification.
