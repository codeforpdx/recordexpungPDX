from os import path
from pathlib import Path
import time

from bs4 import BeautifulSoup
from flask.views import MethodView

from expungeservice.crawler.crawler import Crawler


class CaseDetailPage(MethodView):
    def get(self, id):
        url = f"https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID={id}"

        max_retries = 3
        backoff_seconds = 2
        # Retry loop with backoff
        for attempt in range(max_retries):
            html = Crawler.fetch_link(url)
            if html:
                return CaseDetailPage._strip_links(html)

            if attempt < max_retries - 1:
                time.sleep(backoff_seconds)

        return f"Case detail page with ID of {id} does not exist."

    @staticmethod
    def _strip_links(html):
        soup = BeautifulSoup(html.text, "html.parser")
        for a in soup.findAll("a"):
            a["href"] = "#"
        return soup.prettify()


class CaseDetailPageCSS(MethodView):
    def get(self):
        return Path(path.join(path.dirname(__file__), "resources", "oeci.css")).read_text()


def register(app):
    app.add_url_rule("/api/case_detail_page/<int:id>", view_func=CaseDetailPage.as_view("case_detail_page"))
    app.add_url_rule(
        "/api/case_detail_page/CSS/PublicAccess.css", view_func=CaseDetailPageCSS.as_view("case_detail_page_css")
    )
