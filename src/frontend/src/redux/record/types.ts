import {RecordSummaryType} from '../../components/SearchResults/types'

export interface RecordWrapper {
  record: Record;
}
export interface SearchResponse {
  data: RecordWrapper;
}

export interface Record {
  total_balance_Due?: number;
  cases?: any[];
  errors?: string[];
  summary?: RecordSummaryType;
}

// These constants are used as the 'type' field in Redux actions.
export const SEARCH_RECORD = 'LOAD_SEARCH_RECORD';
export const SEARCH_RECORD_LOADING = 'LOAD_SEARCH_RECORD_LOADING';
export const CLEAR_SEARCH_RECORD = 'CLEAR_SEARCH_RECORD';

export interface SearchRecordState {
  loading: boolean;
  record?: Record;
}

interface SearchRecordAction {
  type:
    | typeof SEARCH_RECORD
    | typeof SEARCH_RECORD_LOADING
    | typeof CLEAR_SEARCH_RECORD;
  search_record: Record;
}

// Add other Action types here like so:
// export type RecordActionTypes = LoadRecordAction | OtherRecordAction;
export type SearchRecordActionType = SearchRecordAction;
