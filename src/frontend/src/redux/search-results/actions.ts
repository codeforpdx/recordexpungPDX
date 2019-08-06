import { LOAD_SEARCH_RECORDS } from '../types';
import getSearchRecords from '../../service/get-records';

export function loadSearchRecords() {
  return {
    type: LOAD_SEARCH_RECORDS,
    search_records: getSearchRecords()
  };
}
