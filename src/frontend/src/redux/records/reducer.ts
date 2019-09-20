import {
  LOAD_SEARCH_RECORDS,
  SearchRecordState,
  SearchRecordsActionType
} from './types';

const initalState: SearchRecordState = {
  records: []
};

export function searchRecordsReducer(
  state = initalState,
  action: SearchRecordsActionType
): SearchRecordState {
  switch (action.type) {
    case LOAD_SEARCH_RECORDS:
      return { records: action.search_records };
    default:
      return state;
  }
}
