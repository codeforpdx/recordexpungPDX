import { Dispatch } from 'redux';
import apiService from '../../service/api-service';
import { AxiosResponse } from 'axios';
import { LOAD_SEARCH_RECORDS, LOAD_SEARCH_RECORDS_LOADING } from './types';

export function loadSearchRecords(
  first_name: string,
  last_name: string,
  birthday: string
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: LOAD_SEARCH_RECORDS_LOADING
    });
    return apiService(dispatch, {
      url: '/api/search',
      data: {
        first_name: first_name,
        middle_name: '',
        last_name: last_name,
        birth_date: birthday
      },
      method: 'post',
      withCredentials: true
    }).then((response: AxiosResponse) => {
      dispatch({
        type: LOAD_SEARCH_RECORDS,
        search_records: response.data.data.record
      });
    });
  };
}
