import {RecordData} from '../../components/RecordSearch/Record/types'

export interface RecordWrapper {
  record: RecordData;
}
export interface SearchResponse {
  data: RecordWrapper;
}

// These constants are used as the 'type' field in Redux actions.
export const SEARCH_RECORD = 'LOAD_SEARCH_RECORD';
export const SEARCH_RECORD_LOADING = 'LOAD_SEARCH_RECORD_LOADING';
export const CLEAR_RECORD = 'CLEAR_RECORD';

export interface SearchRecordState {
  loading: boolean;
  record?: RecordData;
}

interface SearchRecordAction {
  type:
    | typeof SEARCH_RECORD
    | typeof SEARCH_RECORD_LOADING
    | typeof CLEAR_RECORD;
  search_record: RecordData;
}

// Add other Action types here like so:
// export type RecordActionTypes = LoadRecordAction | OtherRecordAction;
export type SearchRecordActionType = SearchRecordAction;
