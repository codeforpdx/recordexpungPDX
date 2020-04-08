import {
  RecordData,
  RecordSummaryData,
  QuestionsData
} from '../../components/RecordSearch/Record/types'

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

export const SEARCH_RECORD = 'SEARCH_RECORD';
export const SEARCH_RECORD_LOADING = 'SEARCH_RECORD_LOADING';
export const CLEAR_RECORD = 'CLEAR_RECORD';
export const SELECT_ANSWER = 'SELECT_ANSWER';

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
  type: typeof SELECT_ANSWER
  answer: string
}

export type SearchRecordActionType = SearchRecordAction | QuestionsAction;
