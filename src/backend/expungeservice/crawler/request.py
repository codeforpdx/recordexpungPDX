class Payload:

    @staticmethod
    def login_payload(username, password):
        return {'UserName': username, 'Password': password, 'ValidateUser': '1', 'dbKeyAuth': 'JusticePA',
                'SignOn': 'Sign+On'}

    @staticmethod
    def payload(param_parser, last_name, first_name, middle_name, birth_date):

        payload = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': param_parser.view_state,
                '__VIEWSTATEGENERATOR': param_parser.view_state_generator,
                '__EVENTVALIDATION': param_parser.event_validation,
                'NodeID': param_parser.node_id,

                'NodeDesc': 'All+Locations',
                'SearchBy': '1',
                'ExactName': 'on',
                'CaseSearchMode': 'CaseNumber',
                'CaseSearchValue': '',

                'CitationSearchValue': '',
                'CourtCaseSearchValue': '',
                'PartySearchMode': 'Name',

                'AttorneySearchMode': 'Name',
                'LastName': last_name,
                'FirstName': first_name,
                'cboState': 'AA',

                'MiddleName': middle_name,
                'DateOfBirth': birth_date,
                'DriverLicNum': '',
                'CaseStatusType': '0',
                'DateFiledOnAfter': '',

                'DateFiledOnBefore': '',
                'chkCriminal': 'on',
                'chkFamily': 'on',
                'chkCivil': 'on',
                'chkProbate': 'on',

                'chkDtRangeCriminal': 'on',
                'chkDtRangeFamily': 'on',
                'chkDtRangeCivil': 'on',
                'chkDtRangeProbate': 'on',

                'chkCriminalMagist': 'on',
                'chkFamilyMagist': 'on',
                'chkCivilMagist': 'on',
                'chkProbateMagist': 'on',

                'DateSettingOnAfter': '',
                'DateSettingOnBefore': '',
                'SortBy': 'fileddate',
                'SearchSubmit': 'Search',

                'SearchType': 'PARTY',
                'SearchMode': 'NAME',
                'NameTypeKy': 'ALIAS',
                'BaseConnKy': 'DF',

                'StatusType': 'true',
                'ShowInactive': '',
                'AllStatusTypes': 'true',
                'CaseCategories': '',

                'RequireFirstName': 'True',
                'CaseTypeIDs': '',
                'HearingTypeIDs': '',
                'SearchParams': "SearchBy~~Search+By:~~Defendant~~Defendant||chkExactName~~Exact+Name:~~on~~on||PartyNameOption~~Party+Search+Mode:~~Name~~Name||LastName~~Last+Name:~~" + last_name + "~~" + last_name + "||FirstName~~First+Name:~~" + first_name + "~~" + first_name + "||MiddleName~~Middle+Name:~~" + middle_name + "~~" + middle_name+ "||DateOfBirth~~Date+of+Birth:~~" + birth_date + "~~" + birth_date + "||AllOption~~All~~0~~All||selectSortBy~~Sort+By:~~Filed+Date~~Filed+Date"

            }

        return payload


class URL:

    @staticmethod
    def login_url():
        return 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/login.aspx'
