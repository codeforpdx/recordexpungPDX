import apiService from '../../service/api-service';
import { Dispatch } from 'redux';
import { LOAD_SEARCH_RECORDS, LOAD_SEARCH_RECORDS_LOADING } from './types';

const fakeRecord = {
  total_balance_due: 199.99,
  cases: [
    {
      name: 'Doe, John',
      birth_year: 1970,
      case_number: 'HA05555555',
      citation_number: 'HA08643443',
      location: 'Multnomah',
      date: '09/05/2008',
      violation_type: 'Municipal Parking',
      current_status: 'Closed',
      charges: [
        {
          name: 'Loading Zone',
          statute: '29',
          level: 'Violation Unclassified',
          date: '09/04/2008',
          disposition: {
            date: '11/18/2008',
            ruling: 'Convicted'
          },
          expungement_result: {
            type_eligibility: false,
            type_eligibility_reason: 'Ineligible under 137.225(5)',
            time_eligibility: null,
            time_eligibility_reason: '',
            date_of_eligibility: null
          }
        }
      ],
      balance_due: 199.99,
      case_detail_link:
        'https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=11918348'
    },
    {
      name: 'Doe, John',
      birth_year: 1970,
      case_number: '18VI55555',
      citation_number: 'RU420001442',
      location: 'Multnomah',
      date: '04/02/2018',
      violation_type: 'Offense Violation',
      current_status: 'Closed',
      charges: [
        {
          name: 'Violating a Speed Limit',
          statute: '811111',
          level: 'Violation Class A',
          date: '03/06/2018',
          disposition: {
            date: '04/02/2018',
            ruling: 'Dismissed'
          },
          expungement_result: {
            type_eligibility: true,
            type_eligibility_reason: 'Eligible under 137.225(1)(b)',
            time_eligibility: null,
            time_eligibility_reason: '',
            date_of_eligibility: null
          }
        },
        {
          name: 'Violation Driving While Suspended or Revoked',
          statute: '811175',
          level: 'Violation Class A',
          date: '03/06/2018',
          disposition: {
            date: '04/02/2018',
            ruling: 'Dismissed'
          },
          expungement_result: {
            type_eligibility: true,
            type_eligibility_reason: 'Eligible under 137.225(1)(b)',
            time_eligibility: null,
            time_eligibility_reason: '',
            date_of_eligibility: null
          }
        }
      ],
      balance_due: 0.0,
      case_detail_link:
        'https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=55555555'
    }
  ]
};

export const loadSearchRecordsMock = () => (dispatch: Dispatch) => {
  dispatch({
    type: LOAD_SEARCH_RECORDS_LOADING
  });
  // search endpoint requires first, middle, last, and birth_date
  return apiService(dispatch, {
    url: '/api/search',
    data: {
      first_name: 'first',
      middle_name: '',
      last_name: 'last',
      birth_date: '10102010'
    },
    method: 'post',
    withCredentials: true,
    authenticated: true
  })
    .then((response: any) => {
      // data returned in the format that will be sent from crawler
      // as `response.data.data`
      dispatch({
        type: LOAD_SEARCH_RECORDS,
        search_records: fakeRecord
      });
    })
    .catch((error: any) => {
      // Request errors ie: unauthenticated as `error.response`
    });
};
