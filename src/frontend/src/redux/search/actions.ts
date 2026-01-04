import { Dispatch } from "redux";
import { AxiosError, AxiosResponse } from "axios";
import fileDownload from "js-file-download";
import apiService from "../../service/api-service";
import store from "../store";
import { stopLoadingSummary } from "../summarySlice";
import { ChargeData } from "../../components/RecordSearch/Record/types";

import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  SearchResponse,
  SELECT_ANSWER,
  EDIT_CASE,
  DELETE_CASE,
  UNDO_EDIT_CASE,
  EDIT_CHARGE,
  DELETE_CHARGE,
  UNDO_EDIT_CHARGE,
  DOWNLOAD_EXPUNGEMENT_PACKET,
  LOADING_EXPUNGEMENT_PACKET_COMPLETE,
  DOWNLOAD_WAIVER_PACKET,
  LOADING_WAIVER_PACKET_COMPLETE
} from "./types";
import {
  RecordData,
  ShortLabel,
} from "../../components/RecordSearch/Record/types";
import { getShortLabel } from "../../components/RecordSearch/Record/util";

function isExludedCharge({ statute, level, name }: ChargeData) {
  const chapter = Number(statute.slice(0, 3));
  const lowerLevel = level.toLowerCase();

  if (name.toLowerCase().includes("pedestrian j-walking")) return true;
  if (level.toLowerCase().includes("infraction")) return true;

  // 813 	Driving Under the Influence of Intoxicants
  if (isNaN(chapter) || chapter === 813) return false;

  if ((chapter >= 801 && chapter <= 826) || [481, 482, 483].includes(chapter)) {
    if (!lowerLevel.includes("felony") && !lowerLevel.includes("misdemeanor")) {
      return true;
    }
  }

  return false;
}

export function processCharges(record: RecordData) {
  if (!record?.cases) return;

  record.cases.forEach((aCase) => {
    const fines = aCase.balance_due;

    aCase.charges.forEach((charge) => {
      const {
        charge_eligibility: { status },
      } = charge.expungement_result;
      charge.shortLabel = getShortLabel(status, null, fines) as ShortLabel;
      charge.isExcluded = isExludedCharge(charge);
    });
  });
}

export function storeSearchResponse(data: SearchResponse, dispatch: Dispatch) {
  if (validateSearchResponseData(data)) {
    const receivedRecord = data.record;
    const record: RecordData = {
      total_balance_due: receivedRecord.total_balance_due,
      cases: receivedRecord.cases,
      errors: receivedRecord.errors,
      summary: receivedRecord.summary,
    };

    processCharges(record);

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
    demo: store.getState().demo.isOn,
    aliases: store.getState().searchForm.aliases,
    today: store.getState().searchForm.date,
    questions: store.getState().search.questions,
    edits: store.getState().search.edits,
  };
}

function buildAndSendSearchRequest(dispatch: any): any {
  return apiService(dispatch, {
    url: store.getState().demo.isOn ? "/api/demo" : "/api/search",
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

export function buildAndSendDownloadPdfRequest(dispatch: any): any {
  return apiService(dispatch, {
    url: "/api/pdf",
    data: buildSearchRequest(),
    method: "post",
    withCredentials: true,
    responseType: "blob",
  })
    .then((response: AxiosResponse) => {
      const filename =
        response.headers["content-disposition"]!.split("filename=")[1].split(
          " "
        )[0];
      fileDownload(response.data, filename);
      dispatch(stopLoadingSummary());
    })
    .catch((error: AxiosError) => {
      dispatch(stopLoadingSummary());
      alert(error.message);
    });
}

export function searchRecord() {
  return (dispatch: Dispatch) => {
    dispatch({
      type: RECORD_LOADING,
    });
    return buildAndSendSearchRequest(dispatch);
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

export function editCase(
  edit_status: string,
  case_number: string,
  status: string,
  restitution: string,
  county: string,
  balance: string,
  birth_year: string
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: EDIT_CASE,
      edit_status,
      case_number,
      restitution,
      status,
      county,
      balance,
      birth_year,
    });
    return buildAndSendSearchRequest(dispatch);
  };
}

export function deleteCase(case_number: string): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: DELETE_CASE,
      case_number,
    });
    return buildAndSendSearchRequest(dispatch);
  };
}

export function undoEditCase(case_number: string): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: UNDO_EDIT_CASE,
      case_number,
    });
    return buildAndSendSearchRequest(dispatch);
  };
}

export function editCharge(
  edit_status: string,
  case_number: string,
  ambiguous_charge_id: string,
  charge_date: string,
  ruling: string,
  disposition_date: string,
  probation_revoked_date: string,
  charge_type: string,
  level: string,
  charge_name: string
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: EDIT_CHARGE,
      edit_status,
      case_number,
      ambiguous_charge_id,
      charge_date,
      ruling,
      disposition_date:
        disposition_date === "" ? charge_date : disposition_date,
      probation_revoked_date,
      charge_type,
      level,
      charge_name,
    });
    return buildAndSendSearchRequest(dispatch);
  };
}

export function deleteCharge(
  case_number: string,
  ambiguous_charge_id: string
): any {
  return (dispatch: Dispatch): any => {
    dispatch({
      type: DELETE_CHARGE,
      case_number,
      ambiguous_charge_id,
    });
    return buildAndSendSearchRequest(dispatch);
  };
}

export function undoEditCharge(
  case_number: string,
  ambiguous_charge_id: string
): any {
  return (dispatch: Dispatch): any => {
    dispatch({
      type: UNDO_EDIT_CHARGE,
      case_number,
      ambiguous_charge_id,
    });
    return buildAndSendSearchRequest(dispatch);
  };
}

export function downloadExpungementPacket(
  name: string,
  dob: string,
  mailingAddress: string,
  phoneNumber: string,
  city: string,
  state: string,
  zipCode: string,
  emailAddress: string
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: DOWNLOAD_EXPUNGEMENT_PACKET,
      name,
      dob,
      mailingAddress,
      phoneNumber,
      city,
      state,
      zipCode,
      emailAddress,
    });
    return apiService(dispatch, {
      url: "/api/expungement-packet",
      data: {
        demo: store.getState().demo.isOn,
        aliases: store.getState().searchForm.aliases,
        questions: store.getState().search.questions,
        edits: store.getState().search.edits,
        today: store.getState().searchForm.date,
        userInformation: store.getState().search.userInformation,
      },
      method: "post",
      withCredentials: true,
      responseType: "blob",
    })
      .then((response: AxiosResponse) => {
        const filename =
          response.headers["content-disposition"]!.split("filename=")[1].split(
            " "
          )[0];
        fileDownload(response.data, filename);
        dispatch({
          type: LOADING_EXPUNGEMENT_PACKET_COMPLETE,
        });
      })
      .catch((error: AxiosError) => {
        alert(error.message);
      });
  };
}

export function downloadWaiverPacket(
  name: string,
  dob: string,
  mailingAddress: string,
  phoneNumber: string,
  city: string,
  state: string,
  zipCode: string,
  explain: string,
  explain2: string,
  snap: boolean,
  ssi: boolean,
  tanf: boolean,
  ohp: boolean,
  custody: boolean,
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: DOWNLOAD_WAIVER_PACKET,
      name,
      dob,
      mailingAddress,
      phoneNumber,
      city,
      state,
      zipCode,
      explain,
      explain2,
      snap,
      ssi,
      tanf,
      ohp,
      custody,
    });
    return apiService(dispatch, {
      url: "/api/waiver-packet",
      data: {
        demo: store.getState().demo.isOn,
        aliases: store.getState().searchForm.aliases,
        questions: store.getState().search.questions,
        edits: store.getState().search.edits,
        today: store.getState().searchForm.date,
        userInformation: store.getState().search.userInformation,
        waiverInformation: store.getState().search.waiverInformation
      },
      method: "post",
      withCredentials: true,
      responseType: "blob",
    })
      .then((response: AxiosResponse) => {
        const filename =
          response.headers["content-disposition"]!.split("filename=")[1].split(
            " "
          )[0];
        fileDownload(response.data, filename);
        dispatch({
          type: LOADING_WAIVER_PACKET_COMPLETE,
        });
      })
      .catch((error: AxiosError) => {
        alert(error.message);
      });
  };
}
