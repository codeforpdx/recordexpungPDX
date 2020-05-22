import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  CLEAR_RECORD,
  SELECT_ANSWER,
  ANSWER_DISPOSITION,
  EDIT_CASE,
  DELETE_CASE,
  UNDO_EDIT_CASE,
  SearchRecordState,
  SearchRecordActionType
} from './types';
import {QuestionsData} from '../../components/RecordSearch/Record/types'

const initalState: SearchRecordState = {
  loading: false,
  aliases: [],
  dispositionWasUnknown: [],
  edits: {},
  nextNewCaseNum: 1
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
      {
        const edits = JSON.parse(JSON.stringify(state.edits));
        edits[action.case_number] = edits[action.case_number] || {"action": "update"};
        edits[action.case_number]["charges"] = edits[action.case_number]["charges"] || {};
        edits[action.case_number]["charges"][action.ambiguous_charge_id] = edits[action.case_number]["charges"][action.ambiguous_charge_id] || {};
        edits[action.case_number]["charges"][action.ambiguous_charge_id]["disposition"] = action.disposition_edit;
        edits[action.case_number]["charges"][action.ambiguous_charge_id]["probation_revoked"] = action.probation_revoked_edit;
        return {...state, edits: edits, loading: true};
      }
    case EDIT_CASE:
      {
        const edits = JSON.parse(JSON.stringify(state.edits));
        if (!((edits[action.case_number] && edits[action.case_number]["action"] == "update") && action.edit_type == "update")) {
          edits[action.case_number] = {"action": action.edit_type}
        } // This check lets edits merge and not overwrite each other (e.g. AnswerDisposition vs EditCase)
        edits[action.case_number]["summary"] = {
          current_status: action.status,
          location: action.county,
          balance_due: action.balance_due,
          birth_year: action.birth_year
        }
        return {...state, nextNewCaseNum: state.nextNewCaseNum + (action.edit_type == "add" ? 1 : 0), edits: edits, loading: true};
      }
    case DELETE_CASE:
      {
        const edits = JSON.parse(JSON.stringify(state.edits));
        edits[action.case_number] = {"action": "delete"};
        return {...state, edits: edits, loading: true};
      }
    case UNDO_EDIT_CASE:
      {
        const edits = (JSON.parse(JSON.stringify(state.edits)));
        const filtered_edits = Object.keys(edits)
          .filter( key => action.case_number !== key )
          .reduce( (res :any, key) => (res[key] = edits[key], res), {} );

        //edits[action.case_number] = {"action": ""};
        return {...state, edits: filtered_edits, loading: true};
      }
    default:
      return state;
  }
}
