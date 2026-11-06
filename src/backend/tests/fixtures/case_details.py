from os import path
from pathlib import Path

CASE_HTMLDIR = path.join(path.dirname(__file__), "case_html")


def read_html(p):
    return Path(path.join(CASE_HTMLDIR, p + ".html")).read_text()


class CaseDetails:
    CASE_X1 = read_html("x1")
    CASE_WITHOUT_FINANCIAL_SECTION = read_html("without_financial_section")
    CASE_WITH_PARTIAL_DISPOS = read_html("with_partial_dispos")
    CASE_WITHOUT_DISPOS = read_html("without_dispos")
    CASE_PARKING_VIOLATION = read_html("parking_violation")
    CASEJD1 = read_html("jd1")
    CASEJD74 = read_html("jd74")
    CASE_X3 = read_html("x3")

    @staticmethod
    def case_x(
        arrest_date="03/12/2017",
        charge1_name="Driving Uninsured",
        charge1_statute="806.010",
        charge1_level="Class B Felony",
        dispo_date="06/12/2017",
        dispo_ruling_1="Convicted - Failure to Appear",
        charge2_level="Class B Felony",
        dispo_ruling_2="Dismissed",
        charge3_level="Class B Felony",
        dispo_ruling_3="Dismissed",
    ):

        return read_html("x").format(**locals())

    @staticmethod
    def event_row(event_date: str, name: str, text: str = "", row_id: str = "RCDER9") -> str:
        """One row of the "OTHER EVENTS AND HEARINGS" list, as OECI renders it."""
        return (
            f'<tr><th class="ssTableHeaderLabel" valign="top" id="{row_id}">{event_date}</th>'
            '<td style="border-right: 1px solid black">&nbsp;</td><td>&nbsp;</td>'
            f'<td headers="COtherEventsAndHearings {row_id}"><b>{name}</b>'
            f'<div style="padding-left: 10px"><i>{text}</i></div>'
            '<div style="padding-left: 10px;font-size:8pt;">Created: 01/01/2020 12:00 AM</div></td></tr>'
        )

    @staticmethod
    def case_x_with_events(rows: list) -> str:
        """case_x with the given (date, name, text) rows appended to its other events, in order."""
        page = CaseDetails.case_x()
        citation_row = page.index('id="RCDER1">')
        insert_at = page.index("</tr>", citation_row) + len("</tr>")
        events = "".join(
            CaseDetails.event_row(event_date, name, text, f"RCDER{i + 2}")
            for i, (event_date, name, text) in enumerate(rows)
        )
        return page[:insert_at] + events + page[insert_at:]

    CASE_WITH_REVOKED_PROBATION = read_html("with_revoked_probation")
    COMMENTS_ENTERED_UNDER_SEPARATE_DISPOSITION_HEADERS = read_html(
        "comments_entered_under_separate_disposition_headers"
    )
    CHARGE_INFO_WITH_EMPTY_DATA_CELLS = read_html("charge_info_with_empty_data_cells")
    CASE_WITH_ODD_EVENT_TABLE_CONTENTS = read_html("case_detail_with_odd_event_table_contents")
    CASE_WITH_SINGLE_DUII = read_html("duii")
    CASE_MJ_CONVICTION = read_html("mj")
    CASE_MJ_AND_TRAFFIC_CONVICTION = read_html("mj_with_traffic")
    CASE_MJ_AND_FUGITIVE_CONVICTION = read_html("mj_with_fugitive")
    CASE_MJ_AND_FELONY_CONVICTION = read_html("mj_with_felony")
