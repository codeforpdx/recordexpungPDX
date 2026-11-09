# Case captions and Washington County contempt motions: design

**Decided with Jordan on 6 November 2026.** Two requests from the CLEAR Clinic, sent 8 October
2026 and chased on 6 November. The clinic's contempt motion template and its caption drawing
are in `private/`, which is never committed.

## Goals

1. Motions name the defendant the way the court's own register does. Umatilla rejected a batch
   of motions because the caption RecordSponge prints is not the case caption.
2. Washington County contempt cases prosecuted by the DOJ Child Support Division are served on
   the DOJ, on the clinic's contempt template. The Washington County DA does not prosecute
   contempt, and the court rejects motions that carry the DA's address.

## Case captions

**What is wrong.** Every motion, the fee waiver, and the PDF file names use the name from the
OECI search results row: "SMITH, CASEY JACKSON", sometimes followed by "Also Known As ..." and
an alias id. The court's caption is the header of the case detail page, under "Register of
Actions": `State of Oregon vs CASEY JACKSON SMITH`.

**What changes.**

- The case detail parser reads that header. The caption name is the text after "vs" (OECI
  writes "vs" or "VS."), whitespace collapsed, otherwise untouched. OECI prints it in capitals
  and the motion prints it the same way.
- `CaseSummary.caption_name`, empty when the page has no header and for cases added in the
  editor. Paperwork falls back to the search-results name when it is empty.
- Paperwork uses it: the 2026 form's defendant line, the Multnomah forms' Defendant field, the
  fee waiver's Defendant field, and the motion file names.
- Nothing on screen changes. The Name column and the record JSON keep the search-results name,
  aliases included, because that is what identifies a person. The field is backend-only: paperwork
  and edits both rebuild the record from the cached scrape, so it survives case edits without a
  round trip through the frontend.

## Washington County contempt

**The prompt.** The classifier already recognizes a charge whose name contains "contempt" as
Contempt of Court. For Washington County only, it now attaches the question "Does this charge
involve child support?" with answers Yes and No, in the charge-question UI the clinic already
uses for ambiguous dispositions and lesser charges. Until it is answered the charge is "Needs
More Analysis", so the case cannot reach paperwork unseen. Yes sets the charge type to Contempt
of Court - Child Support; No leaves it Contempt of Court. Other counties see no question.

**The charge type.** `ContemptOfCourtChildSupport` extends `ContemptOfCourt`: same eligibility,
same severity, type name "Contempt of Court - Child Support". Every check for contempt in form
filling matches it through the subclass. It joins the editor's charge-type list so a user can
set or undo it there too.

**The paperwork.** A case with an eligible child-support contempt charge is filled on the
clinic's template, `oregon_contempt_child_support.pdf`, with the prosecutor address
"Oregon Department of Justice Child Support Division - P.O. Box 14680 - Salem, OR 97309" in the
certificate of mailing. The template has the same 49 fields as the current 2026 form; the only
visible difference is the static heading "No Filing Fee / Contempt of Court - Child Support"
on page one, which is the flag the clinic wants so the motion is not mailed to the DA. Every
other field is filled as today. The file name ends in `_contempt_child_support`.

**Whole case, not whole charge.** If a child-support contempt charge shares a case with other
eligible charges, the whole case goes on the contempt template to the DOJ. Washington files
contempt as its own case type ("Procedural Matters - Contempt of Court Punitive"), so a mixed
case should be rare; the user can split the charges in the editor if one turns up.

## Model and plumbing

| Layer | Change |
| --- | --- |
| `crawler/parsers/case_parser.py` | Parse the caption name from the "State of Oregon vs" header |
| `models/case.py` | `CaseSummary.caption_name: str = ""`; `CaseCreator.create` takes it |
| `crawler/crawler.py` | Copy it onto `CaseSummary` |
| `models/charge_types/contempt_of_court.py` | `ContemptOfCourtChildSupport(ContemptOfCourt)` |
| `charge_classifier.py` | Washington contempt gets the Yes/No question |
| `form_filling.py` | `CaseResults.case_name` is the caption name, falling back to the search-results name; every form's defendant field and the file names already read it; `DOJ_CHILD_SUPPORT_ADDRESS`; `has_child_support_contempt` |
| `form_filling_2026.py` | Template and prosecutor address chosen by `has_child_support_contempt` |
| `waiver_form_filling.py` | Defendant field uses the caption name |
| `files/oregon_contempt_child_support.pdf` | The clinic's template |
| `Record/types.ts` | The new type name in `CHARGE_TYPES` |

## Out of scope

- Who prosecutes contempt in other counties. Only Washington asked.
- Captions on screen or in the summary PDF.
- The Multnomah forms, which have no contempt variant.

## Tests

- `tests/parser/test_case_parser.py`: caption name from the existing fixture pages, which use
  both "vs" and "VS."; empty when the header is missing.
- `tests/test_form_filling_2026.py`: a child-support case picks the template and the DOJ address;
  an ordinary Washington contempt case keeps the DA; the caption name reaches the defendant
  line and falls back to the search-results name.
- `tests/test_form_filling.py`: the Multnomah Case Name field prints the caption name.
- `tests/models/charge_types/test_contempt_of_court.py`: the Washington question and its answers;
  no question elsewhere; the child-support type keeps contempt's eligibility.
