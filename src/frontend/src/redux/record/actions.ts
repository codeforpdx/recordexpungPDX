import { Dispatch } from 'redux';
import apiService from '../../service/api-service';
import { AxiosError, AxiosResponse } from 'axios';
import {
  SEARCH_RECORD,
  SEARCH_RECORD_LOADING,
  SearchResponse,
  CLEAR_SEARCH_RECORD
} from './types';
import {AliasType} from '../../components/RecordSearch/types'

function validateResponseData(data: SearchResponse): boolean {
  return data.hasOwnProperty('data') && data.data.hasOwnProperty('record');
}

export function searchRecord(
  aliases: AliasType[]
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: SEARCH_RECORD_LOADING
    });
    return apiService<SearchResponse>(dispatch, {
      url: '/api/search',
      data: {
        aliases: aliases
      },
      method: 'post',
      withCredentials: true
    })
      .then((response: AxiosResponse<SearchResponse>) => {
        if (validateResponseData(response.data)) {
          dispatch({
            type: SEARCH_RECORD,
            search_record: response.data.data.record
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

export function clearSearchRecord() {
  return {
    type: CLEAR_SEARCH_RECORD
  };
}
