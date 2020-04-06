import {
  SEARCH_RECORD,
  SEARCH_RECORD_LOADING,
  CLEAR_RECORD,
  SELECT_ANSWER,
  EDIT_ANSWER,
  CANCEL_EDIT,
  UPDATE_ANALYSIS,
  SearchRecordState,
  SearchRecordActionType
} from './types';
import {RecordData, QuestionsData} from '../../components/RecordSearch/Record/types'

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
      return { ...state, record: action.record, questions: action.questions, loading: false };
    case SEARCH_RECORD_LOADING:
      // When an API call is made for a record, loading state is toggled to true.
      // while loading state is true, a spinner is rendered on the screen. If loading
      // state is false, and no results were fetched, no "search results found" will be displayed.
      return { ...state, record: {}, questions: {}, loading: true };
    case CLEAR_RECORD:
      return { ...state, record: {}, questions: {}, loading: false };
    case SELECT_ANSWER:
      let questions : QuestionsData = JSON.parse(JSON.stringify(state.questions));
      if (questions && questions[action.ambiguous_charge_id]) {
        questions[action.ambiguous_charge_id].selected_answer=action.selected_answer;
      }
      return {...state, questions: questions};
    case EDIT_ANSWER:
      return state;
    case CANCEL_EDIT:
      return state;
    case UPDATE_ANALYSIS:
      return state;
    default:
      return state;
  }
}
