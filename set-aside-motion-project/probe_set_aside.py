"""Search OECI for each subject and report cases whose court events mention "Set Aside".

Subjects come from stdin, one per line:  first|last|mm/dd/yyyy   (DOB optional).
Credentials come from env OECI_USER / OECI_PASS at run time.
The detail page of every matching case is saved under /tmp/probe/<case_number>.html
inside the container so the event rows can be inspected.
"""
import os
import pathlib
import re
import sys

import requests
from bs4 import BeautifulSoup

from expungeservice.crawler.crawler import Crawler
from expungeservice.crawler.request import URL

OUT = pathlib.Path("/tmp/probe")
OUT.mkdir(exist_ok=True)
SET_ASIDE = re.compile(r"set\s*aside", re.I)

def new_session():
    session = requests.Session()
    login_response = Crawler.attempt_login(session, os.environ["OECI_USER"], os.environ["OECI_PASS"])
    return session, login_response


def search(session, login_response, first, last, dob):
    node_response = Crawler._fetch_search_page(session, URL.search_url(), login_response)
    return Crawler._search_record(session, node_response, URL.search_url(), first, last, "", dob)


session, login_response = new_session()


def event_rows(html):
    """(date, text) for every row in the case's "Events & Orders of the Court" section."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("div", class_="ssCaseDetailSectionTitle", string="Events & Orders of the Court")
    if not title:
        return []
    rows = []
    for node in title.parent.next_siblings:
        parts = getattr(node, "contents", [])
        if len(parts) == 4:
            rows.append((parts[0].get_text(" ", strip=True), parts[3].get_text(" ", strip=True)))
    return rows


for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    first, last, *rest = [part.strip() for part in line.split("|")]
    dob = rest[0] if rest else ""
    # OECI silently drops a session after an aborted fetch, and a dropped session
    # answers every search with zero cases. An empty or failed search gets one
    # retry on a fresh login before it counts as a real empty result.
    result = None
    for attempt in (1, 2):
        try:
            result = search(session, login_response, first, last, dob)
        except Exception as error:
            print(f"!! {first} {last} {dob}: search failed (attempt {attempt}): {error}")
            result = None
        if result is not None and result.cases:
            break
        if attempt == 1:
            session, login_response = new_session()
    if result is None:
        continue
    print(f"== {first} {last} {dob}: {len(result.cases)} cases")
    for case in result.cases:
        try:
            html = Crawler.fetch_link(case.case_detail_link, session).text
        except Exception as error:
            print(f"   {case.case_number}: fetch failed: {error}")
            continue
        hits = [(date, text) for date, text in event_rows(html) if SET_ASIDE.search(text)]
        if hits or SET_ASIDE.search(html):
            (OUT / f"{case.case_number}.html").write_text(html)
            print(f"   ** {case.location} {case.case_number} ({case.violation_type}, {case.current_status})")
            print(f"      {case.case_detail_link}")
            for date, text in hits:
                print(f"      {date}: {text[:160]}")
            if not hits:
                print("      (phrase appears outside the events section)")
        else:
            print(f"   -- {case.location} {case.case_number}: no set-aside event")
