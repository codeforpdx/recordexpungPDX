import {Dispatch} from 'redux';
import store from '../store';
import apiService from '../../service/api-service';
import {AxiosError, AxiosResponse} from 'axios';

import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  SearchResponse,
  CLEAR_RECORD,
  SELECT_ANSWER,
  ANSWER_DISPOSITION
} from './types';
import {AliasData} from '../../components/RecordSearch/SearchPanel/types'
import {RecordData} from '../../components/RecordSearch/Record/types'

function storeSearchResponse(data: SearchResponse, dispatch: Dispatch) {
  if (validateSearchResponseData(data)) {
    const receivedRecord = data.record;
    const record: RecordData = {
      total_balance_due: receivedRecord.total_balance_due,
      cases: receivedRecord.cases,
      errors: receivedRecord.errors,
      summary: receivedRecord.summary,
    };
    dispatch({
      type: DISPLAY_RECORD,
      record: record,
      questions: receivedRecord.questions,
      dispositionWasUnknown: receivedRecord.disposition_was_unknown
    });
  } else {
    alert('Response data has unexpected format.');
  }
}

function validateSearchResponseData(data: SearchResponse): boolean {
  return data.hasOwnProperty('record');
}

function buildAndSendSearchRequest(dispatch: any) : any {
  return apiService<SearchResponse>(dispatch, {
    url: '/api/search',
    data: {
      aliases: store.getState().search.aliases,
      questions: store.getState().search.questions,
      edits: store.getState().search.edits
    },
    method: 'post',
    withCredentials: true
  })
    .then((response: AxiosResponse<SearchResponse>) => {
      storeSearchResponse(response.data, dispatch)
    })
    .catch((error: AxiosError<SearchResponse>) => {
      alert(error.message);
    });
}
export function searchRecord(
  aliases: AliasData[]
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: RECORD_LOADING,
      aliases: aliases
    });
    return buildAndSendSearchRequest(dispatch);
  };
}

export function clearRecord() {
  return {
    type: CLEAR_RECORD
  };
}

export function selectAnswer(
  ambiguous_charge_id: string,
  answer: string
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: SELECT_ANSWER,
      ambiguous_charge_id: ambiguous_charge_id,
      answer: answer
    });
    return buildAndSendSearchRequest(dispatch);

  };
}

export function answerDisposition(
  case_number: string,
  ambiguous_charge_id: string,
  ruling: string,
  date: string,
  probation_revoked_date: string): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: ANSWER_DISPOSITION,
      case_number: case_number,
      ambiguous_charge_id: ambiguous_charge_id,
      disposition_edit: ruling === "Open" ? null : {"date": date, "ruling": ruling}
    });
    return buildAndSendSearchRequest(dispatch);
  };
}
