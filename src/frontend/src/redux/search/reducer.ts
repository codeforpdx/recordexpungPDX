import {
  SEARCH_RECORD,
  SEARCH_RECORD_LOADING,
  SearchRecordState,
  SearchRecordActionType,
  CLEAR_RECORD
} from './types';

const initalState: SearchRecordState = {
  loading: false
};

export function searchReducer(
  state = initalState,
  action: SearchRecordActionType
): SearchRecordState {
  switch (action.type) {
    case SEARCH_RECORD:
      // The new state is the record returned in the
      // action. We ignore existing cases and do not
      // necessarily include them in the new state. This
      // is a "destructive update".
      return { ...state, record: action.record, loading: false };
    case SEARCH_RECORD_LOADING:
      // When an API call is made for a record, loading state is toggled to true.
      // while loading state is true, a spinner is rendered on the screen. If loading
      // state is false, and no results were fetched, no "search results found" will be displayed.
      return { ...state, record: {}, loading: true };
    case CLEAR_RECORD:
      return { ...state, record: {}, loading: false };
    default:
      return state;
  }
}
