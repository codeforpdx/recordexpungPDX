import { Dispatch } from "redux";
import store from "../store";
import apiService from "../../service/api-service";
import { AxiosError, AxiosResponse } from "axios";
import fileDownload from "js-file-download";

import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  SearchResponse,
  CLEAR_RECORD,
  SELECT_ANSWER,
} from "./types";
import { AliasData } from "../../components/RecordSearch/SearchPanel/types";
import { RecordData } from "../../components/RecordSearch/Record/types";

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
    });
  } else {
    alert("Response data has unexpected format.");
  }
}

function validateSearchResponseData(data: SearchResponse): boolean {
  return data.hasOwnProperty("record");
}

function buildSearchRequest() {
  return {
    aliases: store.getState().search.aliases,
    questions: store.getState().search.questions,
    edits: store.getState().search.edits,
  };
}

function buildAndSendSearchRequest(dispatch: any): any {
  return apiService<SearchResponse>(dispatch, {
    url: "/api/search",
    data: buildSearchRequest(),
    method: "post",
    withCredentials: true,
  })
    .then((response: AxiosResponse<SearchResponse>) => {
      storeSearchResponse(response.data, dispatch);
    })
    .catch((error: AxiosError<SearchResponse>) => {
      alert(error.message);
    });
}

export function downloadPdf() {
  return apiService(() => {}, {
    url: "/api/pdf",
    data: buildSearchRequest(),
    method: "post",
    withCredentials: true,
    responseType: "blob",
  })
    .then((response: AxiosResponse) => {
      const filename = response.headers["content-disposition"]
        .split("filename=")[1]
        .split(" ")[0];
      fileDownload(response.data, filename);
    })
    .catch((error: AxiosError) => {
      alert(error.message);
    });
}

export function searchRecord(aliases: AliasData[]): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: RECORD_LOADING,
      aliases: aliases,
    });
    return buildAndSendSearchRequest(dispatch);
  };
}

export function clearRecord() {
  return {
    type: CLEAR_RECORD,
  };
}

export function selectAnswer(
  ambiguous_charge_id: string,
  case_number: string,
  question_id: string,
  answer: string,
  edit: any,
  date: string,
  probation_revoked_date: string = ""
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: SELECT_ANSWER,
      ambiguous_charge_id: ambiguous_charge_id,
      case_number: case_number,
      question_id: question_id,
      answer: answer,
      edit: edit,
      date: date,
      probation_revoked_date: probation_revoked_date,
    });
    return buildAndSendSearchRequest(dispatch);
  };
}
