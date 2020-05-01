import {
  RecordData,
  RecordSummaryData,
  QuestionsData
} from '../../components/RecordSearch/Record/types'
import {AliasData} from "../../components/RecordSearch/SearchPanel/types";

export interface SearchResponse {
  record: RecordEndpointData;
}

export interface RecordEndpointData {
  total_balance_due: number;
  cases: any[];
  errors: string[];
  summary: RecordSummaryData;
  questions: QuestionsData;
  disposition_was_unknown: string[];
}

export const DISPLAY_RECORD = 'DISPLAY_RECORD';
export const RECORD_LOADING = 'RECORD_LOADING';
export const CLEAR_RECORD = 'CLEAR_RECORD';
export const SELECT_ANSWER = 'SELECT_ANSWER';
export const ANSWER_DISPOSITION = 'ANSWER_DISPOSITION';

export interface SearchRecordState {
  loading: boolean;
  aliases: AliasData[];
  record?: RecordData;
  questions?: QuestionsData;
  edits?: any;
  dispositionWasUnknown: string[];
}

interface SearchRecordAction {
  type:
    | typeof DISPLAY_RECORD
    | typeof RECORD_LOADING
    | typeof CLEAR_RECORD;
  aliases: AliasData[];
  record: RecordData;
  questions: QuestionsData;
  dispositionWasUnknown: string[];
}

interface QuestionsAction {
  ambiguous_charge_id: string;
  type: typeof SELECT_ANSWER;
  answer: string;
}

interface AnswerDispositionAction {
  type: typeof ANSWER_DISPOSITION;
  case_number: string;
  ambiguous_charge_id: string;
  disposition_edit: any; // TODO: Properly type
}

export type SearchRecordActionType = SearchRecordAction | QuestionsAction | AnswerDispositionAction;
