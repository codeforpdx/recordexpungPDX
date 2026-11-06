# Prior expungement motions: design

**Decided with Jordan on 6 November 2026.** Evidence from OECI, the event names seen per
county, and the probe recipe are in `oeci-findings.md`. Real names and case numbers stay in
`private/`.

## Goal

A case with a set-aside motion already filed needs no new paperwork and will leave OECI once
the court grants it. RecordSponge treats it like any other case: eligible, in "Eligible Now",
and filed again by "Generate Paperwork". A case whose motion was denied or withdrawn stays in
the ordinary analysis, but whoever refiles should see the last attempt and its dates.

## What the user sees

- **On the case.** A banner: "A motion to set aside this case was filed on _." For a denied
  or withdrawn motion: "... filed on _ and denied on _" or "... and withdrawn on _." Blue for
  an open motion, yellow for a closed one.
- **In the summary**, on screen and in the summary PDF. Cases with an open motion sit in their
  own section, "Motion Previously Filed", colored blue, placed ahead of Needs More Analysis
  and grouped by county like the rest. Denied and withdrawn motions do not move the case; the
  sentence prints under its charge lines in the PDF.
- **In the editor.** A "Set-aside Motion" radio, None / Filed / Denied / Withdrawn, a "Motion
  Filed" date, and a "Motion Denied" or "Motion Withdrawn" date shown for those two. Both
  dates are required when shown. The edit wins over the scrape, and an unrelated edit to the
  case carries the scraped motion through unchanged.
- **In paperwork.** No motion PDF for a case with an open motion. The OSP form's warnings
  sheet gets one bullet per skipped case: "Case X has a set-aside motion filed on _ and was
  skipped." A denied or withdrawn motion is a bullet on that case's own motion sheet.

## Detection

The crawler already fetches every case's detail page and walks "OTHER EVENTS AND HEARINGS"
for probation revocations. Detection reads the same rows, in date order, and adds no
requests.

- A **motion** is a row whose event name contains "motion" and any of "set aside",
  "expunge", "expunction". Rows about setting aside a default judgment have no "motion" in
  the name, which is why the phrase alone is not enough.
- A **resolution** is a later row, dated on or after the motion, that is an "Order - Denial"
  mentioning "set aside", or a "Withdrawal" mentioning "set aside" or "motion".
- **The latest motion governs.** Open if nothing resolves it, otherwise denied or withdrawn.
  A 2009 denial does not resolve a 2023 motion. Earlier cycles are not shown.
- A motion years old with no order after it still counts as open. The date is on screen
  and the editor can clear it.

## Model and plumbing

The restitution flag is the template: scraped per case, overridden by the editor, applied in
the merger as a label override that every consumer downstream already respects.

| Layer | Change |
| --- | --- |
| `crawler/parsers/case_parser.py` | Return the latest motion's filed date and, if resolved, the status and order date |
| `models/case.py` | `CaseSummary.set_aside_motion: Optional[SetAsideMotion]` with `status` (filed, denied, withdrawn), `filed_date`, `resolved_date` |
| `crawler/crawler.py` | Copy it onto `CaseSummary` for every county |
| `record_merger.py` | Open motion: every charge on the case that is not already Ineligible gets `ChargeEligibilityStatus.MOTION_FILED`, label "Motion Previously Filed", as the restitution override does. Denied and withdrawn: no change |
| `charges_summarizer.py` | Own bucket for that label, ahead of Needs More Analysis; it wins over balance, restitution, and "on case with Ineligible charge" |
| `serializer.py` | `"set_aside_motion": {status, filed_date, resolved_date}` or `null` |
| `record_editor.py` | Parse the `set_aside_motion` edit's status and dates |
| `form_filling.py`, `form_filling_2026.py` | A case is filed only when it also has no open motion; the warnings bullets above |
| `pdf/markdown_renderer.py` and templates | New section; the resolved sentence once, under the case's first charges |
| `Record/Case.tsx`, `Record/EditCasePanel.tsx`, `RecordSummary/ChargesList.tsx`, `Record/util.tsx` | Banner, radio and dates, section and color, the short label "Motion Filed" in the expanded view |

The merger override is the hinge. Once the charges carry the label, the summary, badges, PDF,
and paperwork filter follow without knowing about motions.

**Per case only.** A motion changes nothing about the person's other cases, and the case's
convictions keep counting in time analysis, since nothing is sealed until the order is
granted.

## Out of scope

- The warnings sheet is never attached on the 2026 form path, so partial expungements outside
  Multnomah ship without one. That is a separate branch; until it lands, the denied and
  withdrawn bullets appear only where the sheet does.
- Waiting periods after a denial. Dates are shown and the reader judges.
- The SB-819 analyzer.

## Open questions for Michael

1. Denials seen so far are "Order - Denial" events in Marion, Multnomah, and Lane. Do other
   counties record them under another name?
2. Six people have a motion from 2023 to early 2025 with no order after it. Are those
   pending, or do some courts grant without an order before the case disappears?
3. A fresh motion sometimes flips the OECI case status to "Purgable". Does that mean
   anything?

None blocks the build. Each would widen detection, not change the design.

## Tests

- `tests/parser/test_case_parser.py`: detection, on event rows built by
  `CaseDetails.case_x_with_events`: the Marion denial, a Multnomah withdrawal, the Lane
  refile, filings about a motion, and the default-judgment false positive.
- `tests/test_set_aside_motion.py`: the merged record through the summary, the serializer,
  the editor, the paperwork filter and warnings, and the summary PDF.
- `Record/setAsideMotion.test.tsx`: the sentence, the banner, and the editor controls.
