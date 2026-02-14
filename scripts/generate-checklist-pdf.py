"""
Generate the RecordSponge Expungement Checklist PDF.

Requirements: pip install reportlab

Output: src/frontend/public/docs/expungement-checklist.pdf

Run from the project root:
    python scripts/generate-checklist-pdf.py
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Flowable
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "src", "frontend", "public", "docs", "expungement-checklist.pdf")


class CheckboxStep(Flowable):
    """A checkbox followed by step text, vertically aligned."""

    def __init__(self, text, style, checkbox_size=11):
        super().__init__()
        self.text = text
        self.style = style
        self.checkbox_size = checkbox_size
        self._para = Paragraph(text, style)

    def wrap(self, availWidth, availHeight):
        text_width = availWidth - self.checkbox_size - 10
        self._para_w, self._para_h = self._para.wrap(text_width, availHeight)
        self.width = availWidth
        self.height = self._para_h + 4
        return self.width, self.height

    def draw(self):
        para_y = self.height - self._para_h
        self._para.drawOn(self.canv, self.checkbox_size + 10, para_y)

        cb_y = self.height - self._para_h + (self._para_h - self.checkbox_size) / 2 - 1

        self.canv.setStrokeColor(black)
        self.canv.setFillColor(white)
        self.canv.setLineWidth(0.8)
        self.canv.rect(0, max(0, cb_y), self.checkbox_size, self.checkbox_size, fill=1, stroke=1)


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    blue = HexColor("#357edd")
    dark = HexColor("#333333")
    gray = HexColor("#555555")

    title_style = ParagraphStyle("ChecklistTitle", parent=styles["Title"], fontSize=20, textColor=dark, spaceAfter=6)
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=11, textColor=gray, spaceAfter=4)
    step_style = ParagraphStyle("StepStyle", parent=styles["Normal"], fontSize=12, textColor=dark, fontName="Helvetica-Bold", spaceBefore=0, spaceAfter=4, leading=14)
    sub_style = ParagraphStyle("SubStyle", parent=styles["Normal"], fontSize=11, textColor=gray, leftIndent=28, spaceBefore=2, spaceAfter=2)
    note_style = ParagraphStyle("NoteStyle", parent=styles["Normal"], fontSize=11, textColor=gray, spaceBefore=0, spaceAfter=4, borderWidth=1, borderColor=HexColor("#cccccc"), borderPadding=8)

    link_str = 'color="#357edd"'
    story = []

    story.append(Paragraph("RecordSponge Expungement Checklist", title_style))
    story.append(Paragraph("A step-by-step guide to the expungement process", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=blue, spaceAfter=12))

    steps = [
        {
            "title": "Log in to OECI",
            "subs": [
                "You will need an OECI account to search for criminal records.",
                f'Purchase a subscription at <a href="https://www.courts.oregon.gov/services/online/Pages/ojcin-signup.aspx" {link_str}>courts.oregon.gov</a>.',
            ],
        },
        {
            "title": "Search records",
            "subs": [
                "Ensure that Assumptions are met",
                "Search by name and date of birth",
            ],
        },
        {
            "title": "Complete paperwork for expungement",
            "subs": [
                "This includes paperwork to modify financial obligations if applicable",
            ],
        },
        {
            "title": "Obtain fingerprints",
            "subs": [
                "Mail to Oregon State Police",
            ],
        },
        {
            "title": "File paperwork in appropriate courts",
            "subs": [],
        },
    ]

    for i, step in enumerate(steps, 1):
        story.append(Spacer(1, 10))
        story.append(CheckboxStep(f'<b>Step {i}:</b>  {step["title"]}', step_style))
        for sub in step["subs"]:
            story.append(Paragraph(f"\u2022  {sub}", sub_style))

    story.append(Spacer(1, 24))
    story.append(Paragraph(
        f'<b>Note:</b> If new to RecordSponge, confirm results with Michael Zhang at '
        f'<a href="mailto:michael@qiu-qiulaw.com" {link_str}>michael@qiu-qiulaw.com</a>.<br/><br/>'
        f'For further details, visit <a href="https://recordsponge.com/manual" {link_str}>recordsponge.com/manual</a>.',
        note_style,
    ))

    doc.build(story)
    print(f"PDF generated: {os.path.abspath(OUTPUT_PATH)}")


if __name__ == "__main__":
    generate()
