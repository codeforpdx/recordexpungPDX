import { Dispatch } from 'redux';
import apiService from '../../service/api-service';
import { AxiosError, AxiosResponse } from 'axios';
import {
  LOAD_SEARCH_RECORDS,
  LOAD_SEARCH_RECORDS_LOADING,
  SearchResponse,
  CLEAR_SEARCH_RECORDS
} from './types';

function validateResponseData(data: SearchResponse): boolean {
  return data.hasOwnProperty('data') && data.data.hasOwnProperty('record');
}

export function loadSearchRecords(
  firstName: string,
  lastName: string,
  birthday: string
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: LOAD_SEARCH_RECORDS_LOADING
    });
    return apiService<SearchResponse>(dispatch, {
      url: '/api/search',
      data: {
        first_name: firstName,
        middle_name: '',
        last_name: lastName,
        birth_date: birthday
      },
      method: 'post',
      withCredentials: true
    })
      .then((response: AxiosResponse<SearchResponse>) => {
        if (validateResponseData(response.data)) {
          dispatch({
            type: LOAD_SEARCH_RECORDS,
            search_records: response.data.data.record
          });
        } else {
          alert('Response data has unexpected format.');
        }
      })
      .catch((error: AxiosError<SearchResponse>) => {
        alert(error.message);
      });
  };
}

export function clearSearchRecords() {
  return {
    type: CLEAR_SEARCH_RECORDS
  };
}
