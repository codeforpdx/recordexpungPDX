import {
  LOAD_SEARCH_RECORDS,
  SearchRecordState,
  SearchRecordsActionType
} from '../types';

const initalState: SearchRecordState = {
  search_records: []
};

export function searchRecordsReducer(
  state = initalState,
  action: SearchRecordsActionType
): SearchRecordState {
  switch (action.type) {
    case LOAD_SEARCH_RECORDS:
      return { search_records: action.search_records };

    default:
      return state;
  }
}
