import { LOAD_SEARCH_RECORDS } from '../types';
import getSearchRecords from '../../service/get-records';

export function loadSearchRecords() {
  console.log('get records action was invoked');
  return {
    type: LOAD_SEARCH_RECORDS,
    search_records: getSearchRecords()
  };
}
