import { LOAD_SEARCH_RECORDS } from '../types';
import getSearchRecords from '../../service/get-records';

export function loadSearchRecords() {
  console.log('get records action was invoked');
  return {
    type: LOAD_SEARCH_RECORDS,
    search_records: getSearchRecords()
  };
}

export const loadSearchRecordsAction = () => (dispatch: Function) => {
  console.log('loadSearchRecordsAction has been invoked');
  return getSearchRecords()
    .then(results => {
      console.log('results in the action');
      dispatch({
        type: LOAD_SEARCH_RECORDS,
        search_records: results.data
      });
    })
    .catch(error => {
      console.log('error is', error);
    });
};

export const loadSearchRecordsMockAction = () => (dispatch: Function) => {
  dispatch({
    type: LOAD_SEARCH_RECORDS,
    search_records: [
      {
        name: 'WOODS, LAVELLE D',
        birth_year: 1970,
        case_number: 'ZA0081909',
        citation_number: 'ZA0081909',
        location: 'Multnomah',
        date: '07/02/2013',
        violation_type: 'Offense Violation',
        current_status: 'Inactive',
        balance_due: '0',
        charges: ['dui', 'dwi'],
        case_detail_link:
          'https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=9036658'
      }
    ]
  });
};
