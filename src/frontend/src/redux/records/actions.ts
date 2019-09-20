import { LOAD_SEARCH_RECORDS } from '../types';
import getSearchRecords from '../../service/get-records';

export const loadSearchRecords = () => (dispatch: Function) => {
  return getSearchRecords()
    .then(results => {
      dispatch({
        type: LOAD_SEARCH_RECORDS,
        search_records: results.data
      });
    })
    .catch(error => {
      dispatch({
        type: LOAD_SEARCH_RECORDS,
        search_records: [{ error: error.message }]
      });
    });
};
