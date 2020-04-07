import { Dispatch } from 'redux';
import apiService from '../../service/api-service';
import { AxiosError, AxiosResponse } from 'axios';
import {
  SEARCH_RECORD,
  SEARCH_RECORD_LOADING,
  SearchResponse,
  CLEAR_RECORD
} from './types';
import {AliasData} from '../../components/RecordSearch/SearchPanel/types'

function validateResponseData(data: SearchResponse): boolean {
  return data.hasOwnProperty('record');
}

export function searchRecord(
  aliases: AliasData[]
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
            record: response.data.record
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

export function clearRecord() {
  return {
    type: CLEAR_RECORD
  };
}
