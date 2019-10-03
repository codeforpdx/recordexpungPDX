import {
  LOAD_SEARCH_RECORDS,
  SearchRecordState,
  SearchRecordsActionType
} from './types';

const initalState: SearchRecordState = {
  records: []
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
      return { records: action.search_records };
    default:
      return state;
  }
}
