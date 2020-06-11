import {
  RecordData,
  RecordSummaryData,
  QuestionsData,
} from "../../components/RecordSearch/Record/types";
import { AliasData } from "../../components/RecordSearch/SearchPanel/types";

export interface SearchResponse {
  record: RecordEndpointData;
}

export interface RecordEndpointData {
  total_balance_due: number;
  cases: any[];
  errors: string[];
  summary: RecordSummaryData;
  questions: QuestionsData;
}

export const DISPLAY_RECORD = "DISPLAY_RECORD";
export const RECORD_LOADING = "RECORD_LOADING";
export const CLEAR_RECORD = "CLEAR_RECORD";
export const SELECT_ANSWER = "SELECT_ANSWER";

export interface SearchRecordState {
  loading: string;
  aliases: AliasData[];
  record?: RecordData;
  questions?: QuestionsData;
  edits?: any;
}

interface SearchRecordAction {
  type: typeof DISPLAY_RECORD | typeof RECORD_LOADING | typeof CLEAR_RECORD;
  aliases: AliasData[];
  record: RecordData;
  questions: QuestionsData;
}

export interface QuestionsAction {
  type: typeof SELECT_ANSWER;
  ambiguous_charge_id: string;
  case_number: string;
  question_id: string;
  answer: string;
  edit: any;
  date: string;
  probation_revoked_date: string;
}

export type SearchRecordActionType = SearchRecordAction | QuestionsAction;
