import { LOAD_SEARCH_RECORDS } from '../types';
import getSearchRecords from '../../service/get-records';

const fakeRecord = [
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
];

export const loadSearchRecords = () => (dispatch: Function) => {
  return getSearchRecords()
    .then(results => {
      dispatch({
        type: LOAD_SEARCH_RECORDS,
        search_records: results.data
      });
    })
    .catch(error => {
      console.log('error is', error);
      return error;
    });
};

//make sure that we dont have somethign redundant
export const loadSearchRecordsMock = () => (dispatch: Function) => {
  return Promise.resolve(fakeRecord).then(payload => {
    console.log('payload', payload);
    dispatch({
      type: LOAD_SEARCH_RECORDS,
      search_records: payload
    });
  });
};

//move mock on own place
