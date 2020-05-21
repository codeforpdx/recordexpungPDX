import {Dispatch} from 'redux';
import store from '../store';
import apiService from '../../service/api-service';
import {AxiosError, AxiosResponse} from 'axios';
import fileDownload from 'js-file-download';

import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  SearchResponse,
  CLEAR_RECORD,
  SELECT_ANSWER,
  ANSWER_DISPOSITION,
  UPDATE_CASE
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

function buildSearchRequest() {
  return {
    aliases: store.getState().search.aliases,
    questions: store.getState().search.questions,
    edits: store.getState().search.edits
  };
}

function buildAndSendSearchRequest(dispatch: any) : any {
  return apiService<SearchResponse>(dispatch, {
    url: '/api/search',
    data: buildSearchRequest(),
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

export function downloadPdf() {
  return apiService(()=>{}, {
    url: '/api/pdf',
    data: buildSearchRequest(),
    method: 'post',
    withCredentials: true,
    responseType: 'blob'
  })
    .then((response: AxiosResponse) => {
      const filename = response.headers["content-disposition"].split("filename=")[1].split(" ")[0];
      fileDownload(response.data, filename)
    })
    .catch((error: AxiosError) => {
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
    const disposition = () => {
      if (ruling === "Unknown") {
        return;
      } else if (ruling === "revoked") {
        return {"date": date, "ruling": "Convicted"};
      } else {
        return {"date": date, "ruling": ruling};
      }
    };
    dispatch({
      type: ANSWER_DISPOSITION,
      case_number: case_number,
      ambiguous_charge_id: ambiguous_charge_id,
      probation_revoked_edit: probation_revoked_date,
      disposition_edit: disposition()
    });
    return buildAndSendSearchRequest(dispatch);
  };
}

export function updateCase(
  case_number: string,
  status: string,
  county: string,
  balance_due: string,
  birth_year: string): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: UPDATE_CASE,
      case_number: case_number,
      status: status,
      county: county,
      balance_due: balance_due,
      birth_year: birth_year
    });
    return buildAndSendSearchRequest(dispatch);
  };
}
