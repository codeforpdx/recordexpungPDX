# Set-aside motions: OECI findings and tooling

The October 2026 research behind `design.md`, which holds the decisions. Section 1 is the
evidence from OECI, section 5 the questions for Michael, section 6 the probe recipe.

A case with a set-aside motion already filed is in a different state from every other
case RecordSponge shows. The motion is in the court's hands, so the case needs no new
paperwork, and once the court grants it the case disappears from OECI altogether. Today
the analysis treats such a case like any other: its charges are labeled eligible, it
lands in "Eligible Now", and "Generate Paperwork" files a second motion for it.

A case whose motion was denied is different again: it stays in the ordinary analysis,
but whoever refiles should know the last attempt failed and when.

This feature:

1. Detects set-aside motions, and their denials, in a case's court events.
2. Shows the motion on the case: open, or filed and rejected with both dates.
3. Puts cases with an open motion in their own summary group, on the panel and in the
   summary PDF, and keeps them out of paperwork.
4. Prints the rejected sentence under the case in the summary PDF and on the warnings
   sheet of the new motion for that case.
5. Lets the case editor set the state by hand: none, open, or rejected, with dates.

Decisions below were made with Jordan on 16 October 2026. The word on screen is
"motion", as in OECI and on the clinic's form.

## 1. What OECI shows

The case detail page lists court events under "Events & Orders of the Court", split into
"DISPOSITIONS" and "OTHER EVENTS AND HEARINGS". The crawler already fetches this page for
every case and walks both lists for dispositions and probation revocations, so detection
adds no requests.

The event name starts with "Motion - Set Aside" and clerks append free text after it.
Across 46 motions found in Marion, Polk, Lincoln, Linn, Lane, Clackamas, Columbia,
Washington, and Multnomah, the names seen are:

| Event name | Where |
| --- | --- |
| Motion - Set Aside | most counties |
| Motion - Set Aside record of arrest / Arrest / arrest / ARREST | Multnomah |
| Motion - Set Aside Conviction | Multnomah |
| Motion - Set Aside and Declaration (in Support) | Clackamas, Columbia |
| Motion - Set Aside **Partial count 2 only** | Washington, for a partial set-aside |

A "Hearing - Set Aside" row can follow the motion.

**Denials** appear as an "Order - Denial" event whose text names the motion, in three
spellings so far: "mo/set aside" (Marion), "motion to set aside" (Multnomah), and
"Comment: motion to set aside" (Lane). The district attorney's objection shows up
before it as "Objection" (Marion) or as "Notice  Opposition to def's motions to set
aside" plus "Memorandum - Opposing Motion" (Multnomah), or "Response ... OPPOSES" (Lane).

**Withdrawals** appear as a "Withdrawal" event with text such as "To withdraw motion to
set aside", "was originally filed as Motion - To withdraw motion to set aside", or just
"set aside" (all Multnomah, all from one clinic batch in late 2024).

**Refiling after a denial** happens: a Lane felony has a motion denied in 2009 and a new
motion in 2023. The 2009 order must not count as resolving the 2023 motion.

**Not a set-aside motion.** "Set aside" also appears in rows about setting aside a
default judgment on a traffic violation, both in a converted disposition ("Status: Set
Aside on: ...") and in an "Order ... set aside default judgment and dismiss" row, and
in hearing rows. None of these has "Motion" in the event name, which is why detection
keys on motion events rather than on the phrase alone.

The Marion denial runs:

```
02/18/2026 | Motion - Set Aside                                   Created: 02/19/2026
06/05/2026 | Objection
06/26/2026 | Letter   Request to appear remotely for objection hearing
06/26/2026 | Order - Allow (Judicial Officer: ...)   Remote appearance
08/21/2026 | Hearing - Objection (11:00 AM)
08/24/2026 | Order - Denial (Judicial Officer: ...)   mo/set aside   Signed: 08/21/2026
```

The row's markup is the standard event row: a `<th class="ssTableHeaderLabel">` holding
the date, two spacer cells, then a `<td>` whose first child is a bold link to the filed
document and whose last child is a small "Created:" line.

```html
<tr>
  <th class="ssTableHeaderLabel" id="RCDER53" valign="top">02/18/2026</th>
  <td style="border-right: 1px solid black"> </td><td> </td>
  <td headers="COtherEventsAndHearings RCDER53">
    <b><a href="CPR.aspx?CaseID=...&EventID=...&CaseCategoryKeys=CR">Motion - Set Aside</a></b>
    <div style="padding-left: 10px;font-size:8pt;">Created: 02/19/2026 10:22 AM</div>
  </td>
</tr>
```

Most motions found were filed in July through September 2026 with no later event. But
old motions with no later event are common too: of the 18 people with a motion, six have
one from 2023 to early 2025 with nothing after it, in Linn, Lane, Clackamas, Columbia,
and Lincoln. Either the clerk never recorded the order or the motion was abandoned. Such
a motion counts as open all the same. The filed date is on screen, and the editor can
clear the state, so the reader draws the conclusion.

Several cases with a fresh motion show the OECI status "Purgable" in place of "Closed".
Whether that is the court's own mark of a pending set-aside is a question for Michael.

Case numbers and the subjects they belong to are in `private/examples.md`.

## 2. Detection rule

Within the case's "OTHER EVENTS AND HEARINGS" rows, in date order:

- A **motion event** is a row whose event name contains "motion" and one of "set aside",
  "expunge", or "expunction", case-insensitively. The last two cover juvenile and older
  wording.
- A **resolving event** is a later row that is either an "Order - Denial" whose text
  mentions "set aside", or a "Withdrawal" whose text mentions "set aside" or "motion".
  A withdrawal resolves the motion the same way a denial does: the case returns to
  ordinary analysis and the case shows the motion as withdrawn rather than rejected.
- The **latest motion governs**. The case has an **open motion** when the latest motion
  has no resolving event after it, and a **rejected motion** when it does. Only events
  dated on or after the latest motion can resolve it, so a 2009 denial leaves a 2023
  motion open. Earlier cycles on the same case are not shown.

A denied motion changes nothing in the eligibility analysis. Whether a denial imposes a
waiting period before refiling is out of scope: dates are shown and the reader judges.

## 3. The restitution flag is the template

Restitution is a per-case boolean scraped from the same detail page, shown on the case,
overridden by the editor, and applied as a post-analysis label override that every
downstream consumer respects. Each layer of this feature does what the restitution flag
does there.

| Layer | Restitution today | Set-aside motion |
| --- | --- | --- |
| Parser `crawler/parsers/case_parser.py` | `restitution = "restitution" in soup.text.lower()` | Walk the event rows; return the latest motion's filed date and, if resolved, the order's date |
| Crawler `crawler/crawler.py` | Copies the flag onto `CaseSummary`, limited to Multnomah and Washington | Copies the motion onto `CaseSummary`, all counties |
| Model `models/case.py` | `CaseSummary.restitution: bool` | `CaseSummary.set_aside_motion: Optional[SetAsideMotion]` with `filed_date`, `resolved_date`, and `status` of `open`, `rejected`, or `withdrawn` |
| Merger `record_merger.py` | Overrides every non-ineligible charge on the case to `INELIGIBLE_IF_RESTITUTION_OWED`, "Ineligible If Restitution Owed" | Overrides every charge on a case with an open motion to `OPEN_SET_ASIDE_MOTION`, "Open Expungement Motion"; rejected motions change nothing |
| Summarizer `charges_summarizer.py` | Status sorts into the "Needs More Analysis / Restitution Owed" bucket | Own bucket, "Open Expungement Motion", ahead of Needs More Analysis; wins over balance, restitution, and "on case with Ineligible charge" |
| Serializer `serializer.py` | `"restitution": case.restitution` | `"set_aside_motion": {status, filed_date, resolved_date}` or `null` |
| Editor `record_editor.py` | `restitution` edit parsed as `value == "True"`; the edit wins over the scraped value | `set_aside_motion` edit with status and dates; the edit wins |
| Case view `Record/Case.tsx` | Banner "Eligible charges are ineligible if restitution is owed" | Open: banner "A motion to set aside this case was filed on _". Rejected: "A motion to set aside this case was filed on _ and rejected on _". Withdrawn: same sentence with "withdrawn" |
| Edit panel `Record/EditCasePanel.tsx` | "Restitution Owed" True/False radio | "Set-aside motion" radio None / Open / Rejected / Withdrawn, a filed-date field, and a resolved-date field shown for Rejected and Withdrawn |
| Summary panel `RecordSummary/ChargesList.tsx` | Colors by section label | New section with its own color |
| Summary PDF `pdf/markdown_renderer.py` and `templates/` | Sections mirror the summarizer | New section, grouped by county like the rest; the rejected sentence printed under the case's charge lines |
| Paperwork `form_filling_2026.py` | A case is filed when it has eligible charges and no balance | Also requires no open motion |
| Warnings sheet `form_filling.py` | One trigger, a partial expungement | The rejected sentence on the new motion for that case; a bullet for every skipped open-motion case on the OSP form's sheet |

The merger override is the hinge. Once the charges on an open-motion case carry the new
status, the summarizer, the badges, the PDF, and the paperwork filter all follow without
each needing to know about motions.

**Per case only.** A motion on one case changes nothing about the person's other cases:
their eligibility, their paperwork, and their part in time analysis. The open case's
convictions keep counting in time analysis too, since nothing is sealed until the order
is granted.

**Out of scope.** The SB-819 analyzer is untouched. Waiting periods after a denial are
not modeled.

## 4. The warnings sheet

The paperwork generator prepends a sheet to a motion PDF headed "Warnings from
RecordSponge", with "Do not submit this page to the District Attorney's office" and
bullet warnings. `FormFilling._generate_warnings_text` builds it, and
`FormFilling._create_and_write_pdf` attaches it.

The 2026 form path in `form_filling_2026.py` sets the partial-expungement flag for the
sheet but writes the PDF without ever calling the warnings generator. Only the Multnomah
fallback and the OSP form still go through the old path that attaches it, so a partial
expungement outside Multnomah ships with no sheet. Restoring the sheet on the 2026 path
is the first commit of this feature; the rejected-motion bullet cannot appear anywhere
outside Multnomah without it.

Open-motion cases produce no motion PDF, so their warning goes on the OSP form's sheet,
the one record-level document in the packet: "Case X has an open expungement motion
filed on _ and was skipped." Whether the summary PDF alone would do instead is undecided.

## 5. Questions for Michael

1. Denials we have seen are "Order - Denial" events in Marion, Multnomah, and Lane. Do
   any counties record a denial under a different event name?
2. Six people have a motion from 2023 to early 2025 with no order after it, in Linn,
   Lane, Clackamas, Columbia, and Lincoln. Are those still pending, or do some courts
   grant without an order appearing before the case disappears?
3. A fresh motion sometimes flips the case status to "Purgable". Does that mean
   anything to you?

## 6. Tooling

**OECI probe.** `probe_set_aside.py` in this folder logs in to OECI with the app's own
crawler, searches each subject, fetches every case detail page, and prints any event row
mentioning "set aside" along with the case's county, number, type, and status. It saves
the raw page of each hit under `probe/` in the container's temp directory. An empty or failed
search gets one retry on a fresh login, because OECI silently drops a session after an
aborted fetch and a dropped session answers every search with zero cases.

It runs inside the project's Docker stack, which carries the pinned Python and the
crawler's dependencies. Subjects go in a file, one per line as `first|last|mm/dd/yyyy`,
with the birth date optional and OECI wildcards allowed in names (`Ta*|To*|5/24/1987`).
Credentials go in an env file with `OECI_USER=` and `OECI_PASS=` lines. Keep both files
outside the repo and out of the command line:

```sh
docker compose up -d expungeservice
docker compose cp set-aside-motion-project/probe_set_aside.py expungeservice:/tmp/probe_set_aside.py
docker exec -i --env-file "$SECRETS/oeci.env" -w /src/backend \
  recordexpungpdx-expungeservice-1 pipenv run python /tmp/probe_set_aside.py < "$SECRETS/subjects.txt"
docker cp recordexpungpdx-expungeservice-1:/tmp/probe/<case_number>.html "$SECRETS/"
```

Jordan supplies the OECI login on request; it is not stored anywhere in the repo.

**Finding subjects.** The clinic and Michael Zhang send Jordan names and birth dates in
bug reports and eligibility questions. The Gmail query
`from:clear-clinic.org OR from:"Michael Zhang"` (Michael writes from qiu-qiulaw.com)
returns about 480 threads, most of them meetings; the names sit in threads whose subjects
mention RecordSponge, RS, a bug, or a record. The referral table mined from that mail is
`private/referrals.md`.

**Private outputs.** The subject list, the referral table, the examples report with case
numbers, probe logs, and saved case pages hold real people's data. They live in
`private/` beside this file, which git ignores, and nowhere else in the repo.
