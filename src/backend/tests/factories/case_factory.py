from expungeservice.models.case import Case, CaseCreator, CaseSummary


class CaseSummaryFactory:
    @staticmethod
    def create(
        info=["John Doe", "1990"],
        case_number="1",
        district_attorney_number="",
        sid="",
        citation_number=None,
        date_location=["1/1/1995", "Multnomah"],
        type_status=["Offense Misdemeanor", "Closed"],
        case_detail_link="?404",
        restitution=False,
        balance="0",
    ) -> CaseSummary:
        return CaseCreator.create(
            info,
            case_number,
            district_attorney_number,
            sid,
            citation_number,
            date_location,
            type_status,
            case_detail_link,
            restitution,
            balance,
        )


class CaseFactory:
    @staticmethod
    def create(
        info=["John Doe", "1990"],
        case_number="1",
        district_attorney_number="",
        sid="",
        citation_number=None,
        date_location=["1/1/1995", "Multnomah"],
        type_status=["Offense Misdemeanor", "Closed"],
        charges=[],
        case_detail_link="?404",
        restitution=False,
        balance="0",
    ) -> Case:
        case_summary = CaseSummaryFactory.create(
            info,
            case_number,
            district_attorney_number,
            sid,
            citation_number,
            date_location,
            type_status,
            case_detail_link,
            restitution,
            balance,
        )
        return Case(case_summary, tuple(charges))
