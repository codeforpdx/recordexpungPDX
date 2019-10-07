import {
  LOAD_SEARCH_RECORDS,
  LOAD_SEARCH_RECORDS_LOADING,
  SearchRecordState,
  SearchRecordsActionType
} from './types';

const initalState: SearchRecordState = {
  loading: false
};

export function recordsReducer(
  state = initalState,
  action: SearchRecordsActionType
): SearchRecordState {
  switch (action.type) {
    case LOAD_SEARCH_RECORDS:
      // The new state is the records returned in the
      // action. We ignore existing records and do not
      // necessarily include them in the new state. This
      // is a "destructive update".
      return { ...state, records: action.search_records, loading: false };
    case LOAD_SEARCH_RECORDS_LOADING:
      // When an API call is made for records, loading state is toggled to true.
      // while loading state is true, a spinner is rendered on the screen. If loading
      // state is false, and no records were fetched, no search results found will be displayed.
      return { ...state, loading: true };
    default:
      return state;
  }
}
