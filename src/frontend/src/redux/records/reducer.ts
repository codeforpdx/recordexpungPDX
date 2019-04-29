import { RecordsState, LOAD_RECORDS, RecordActionTypes } from './types';

const initialState: RecordsState = {
  records: []
};

export function recordsReducer(
  state = initialState,
  action: RecordActionTypes,
): RecordsState {
  switch (action.type) {
    case LOAD_RECORDS:
      // The new state is the records returned in the
      // action. We ignore existing records and do not
      // necessarily include them in the new state. This
      // is a "destructive update".
      return {
        records: action.records
      }
     default:
       return state;
  }
}
