// This data model is based off the UI at http://dev.huntermarcks.net/search/
// I'm not sure about the relationship between "time" and "type". It looks like "time"
// is the future time of eligibility subject to conditions (e.g. no conviction within the
// past three years).
//
// Pasted from the UI:
//
// Time: Eligible now
// Type: Eligible 137.225(5)(b)
// Charge: 4759924B - Poss Controlled Sub 2
// Disposition: Convicted
// Convicted: 2/12/1987
// Case: ZA0061902
// Case Balance: None

export interface Record {
  total_balance_Due?: number;
  cases?: any[];
}

// These constants are used as the 'type' field in Redux actions.
export const LOAD_SEARCH_RECORDS = 'LOAD_SEARCH_RECORDS';
export const LOAD_SEARCH_RECORDS_LOADING = 'LOAD_SEARCH_RECORDS_LOADING';

export interface SearchRecordState {
  loading: boolean;
  records?: Record;
}

interface SearchRecordsAction {
  type: typeof LOAD_SEARCH_RECORDS | typeof LOAD_SEARCH_RECORDS_LOADING;
  search_records: Record;
}

// Add other Action types here like so:
// export type RecordActionTypes = LoadRecordsAction | OtherRecordsAction;
export type SearchRecordsActionType = SearchRecordsAction;

export type CaseProps = {
  case: {
    name: string;
    case_number: string;
    birth_year: number;
    balance_due: number;
  };
};
