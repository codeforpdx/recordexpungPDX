import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  CLEAR_RECORD,
  SELECT_ANSWER,
  SearchRecordState,
  SearchRecordActionType, ANSWER_DISPOSITION
} from './types';
import {QuestionsData} from '../../components/RecordSearch/Record/types'

const initalState: SearchRecordState = {
  loading: false,
  aliases: [],
  dispositionWasUnknown: []
};

export function searchReducer(
  state = initalState,
  action: SearchRecordActionType
): SearchRecordState {
  switch (action.type) {
    case DISPLAY_RECORD:
      return {
        ...state,
        record: action.record,
        questions: action.questions,
        loading: false,
        dispositionWasUnknown: action.dispositionWasUnknown
      };
    case RECORD_LOADING:
      return {...state, record: {}, aliases: JSON.parse(JSON.stringify(action.aliases)), questions: {}, loading: true};
    case CLEAR_RECORD:
      return {...state, record: {}, aliases: [], questions: {}, loading: false};
    case SELECT_ANSWER:
      let questions: QuestionsData = JSON.parse(JSON.stringify(state.questions));
      if (questions && questions[action.ambiguous_charge_id]) {
        questions[action.ambiguous_charge_id].answer = action.answer;
      }
      return {...state, questions: questions, loading: true};
    case ANSWER_DISPOSITION:
      return {...state, loading: true};
    default:
      return state;
  }
}
