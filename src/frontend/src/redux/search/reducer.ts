import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  CLEAR_RECORD,
  SELECT_ANSWER,
  SearchRecordState,
  SearchRecordActionType
} from './types';
import {QuestionsData} from '../../components/RecordSearch/Record/types'

const initalState: SearchRecordState = {
  loading: false
};

export function searchReducer(
  state = initalState,
  action: SearchRecordActionType
): SearchRecordState {
  switch (action.type) {
    case DISPLAY_RECORD:
      // The new state is the record returned in the
      // action. We ignore existing cases and do not
      // necessarily include them in the new state. This
      // is a "destructive update".
      return {
        ...state,
        record: action.record,
        questions: action.questions,
        loading: false
      };
    case RECORD_LOADING:
      // When an API call is made for a record, loading state is toggled to true.
      // while loading state is true, a spinner is rendered on the screen. If loading
      // state is false, and no results were fetched, no "search results found" will be displayed.
      // return { ...state, record: {}, questions: {}, loading: true };
      return {...state, loading: true};
    case CLEAR_RECORD:
      return {...state, record: {}, questions: {}, loading: false};
    case SELECT_ANSWER:
      let questions: QuestionsData = JSON.parse(JSON.stringify(state.questions));
      if (questions && questions[action.ambiguous_charge_id]) {
        questions[action.ambiguous_charge_id].answer = action.answer;
      }
      return {...state, questions: questions, loading: true};
    default:
      return state;
  }
}
