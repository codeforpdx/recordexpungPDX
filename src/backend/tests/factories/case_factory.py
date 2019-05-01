from expungeservice.crawler.models.case import Case


class CaseFactory:

    @staticmethod
    def create(info=['John Doe', '1990'],
               case_number='C0000',
               citation_number=None,
               date_location=['1/1/1995', 'Multnomah'],
               type_status=['Misdemeanor', 'Offense Misdemeanor'],
               charges=[],
               case_detail_link='?404'):

        return Case(info, case_number, citation_number, date_location, type_status, charges, case_detail_link)
