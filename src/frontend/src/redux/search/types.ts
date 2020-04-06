import {RecordData, RecordSummaryData, QuestionsData} from '../../components/RecordSearch/Record/types'

export interface SearchResponse {
  record: RecordEndpointData;
}

export interface RecordEndpointData {
  total_balance_due: number;
  cases: any[];
  errors: string[];
  summary: RecordSummaryData;
  questions: QuestionsEndpointData;
}

export interface QuestionsEndpointData {
    [ambiguous_charge_id: string] : QuestionEndpointData;
}

export interface QuestionEndpointData {
  ambiguous_charge_id: string;
  question: string;
  answer: string;
  options: {[option: string]: string;};
}

export const SEARCH_RECORD = 'SEARCH_RECORD';
export const SEARCH_RECORD_LOADING = 'SEARCH_RECORD_LOADING';
export const CLEAR_RECORD = 'CLEAR_RECORD';
export const SELECT_ANSWER = 'SELECT_ANSWER';
export const EDIT_ANSWER = 'EDIT_ANSWER';
export const CANCEL_EDIT = 'CANCEL_EDIT';
export const UPDATE_ANALYSIS = 'UPDATE_ANALYSIS';

export interface SearchRecordState {
  loading: boolean;
  record?: RecordData;
  questions?: QuestionsData
}

interface SearchRecordAction {
  type:
    | typeof SEARCH_RECORD
    | typeof SEARCH_RECORD_LOADING
    | typeof CLEAR_RECORD;
  record: RecordData;
  questions: QuestionsData;
}

interface QuestionsAction {
  ambiguous_charge_id: string,
  type:
    | typeof SELECT_ANSWER
    | typeof EDIT_ANSWER
    | typeof CANCEL_EDIT
    | typeof UPDATE_ANALYSIS
  selected_answer: string

}
// Add other Action types here like so:
// export type RecordActionTypes = LoadRecordAction | OtherRecordAction;
export type SearchRecordActionType = SearchRecordAction | QuestionsAction;
