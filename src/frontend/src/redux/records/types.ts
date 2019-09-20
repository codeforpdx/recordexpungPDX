export interface Record {
  time: string;
  type: string;
  charge: string;
  disposition: string;
  convicted: number;
  case: string;
  caseBalance: string;
}

export const LOAD_SEARCH_RECORDS = 'LOAD_SEARCH_RECORDS';

export interface SearchRecordState {
  records: Record[];
}

interface SearchRecordsAction {
  type: string;
  search_records: Record[];
}

export type SearchRecordsActionType = SearchRecordsAction;
