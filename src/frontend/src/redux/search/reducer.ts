import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  CLEAR_RECORD,
  SELECT_ANSWER,
  SearchRecordState,
  SearchRecordActionType
} from './types';
import {
  QuestionData,
  QuestionsData
} from '../../components/RecordSearch/Record/types'

const initalState: SearchRecordState = {
  loading: "",
  aliases: [],
  edits: {}
};

function findQuestion(question: QuestionData, question_id: string): null | QuestionData {
  if (question.question_id == question_id) {
    return question;
  } else {
    for (const answer of Object.values(question.options)) {
      if (answer.question) {
        const result = findQuestion(answer.question, question_id);
        if (result) {
          return result;
        }
      }
    }
    return null;
  }
}

function clearSelection(question: QuestionData) {
  question.selection = "";
  for (const answer of Object.values(question.options)) {
      if (answer.question) {
        clearSelection(answer.question);
      }
  }
}

function replaceDispositionDate(question: QuestionData, date: string) {
  for (const answer of Object.values(question.options)) {
    if (answer.edit && answer.edit.disposition) {
      // @ts-ignore
      answer.edit["disposition"]["date"] = date;
    }
    if (answer.question) {
      replaceDispositionDate(answer.question, date);
    }
  }
}

function replaceProbationRevokedDate(question: QuestionData, probation_revoked_date: string) {
  for (const answer of Object.values(question.options)) {
      if (answer.edit && answer.edit.probation_revoked) {
        answer.edit["probation_revoked"] = probation_revoked_date;
      }
      if (answer.question) {
        replaceProbationRevokedDate(answer.question, probation_revoked_date);
      }
  }
}

function replaceDatesInEdit(edit: any, date: string, probation_revoked_date: string) {
  if (edit && edit.disposition && date !== "") {
    edit["disposition"]["date"] = date;
  }
  if (edit && edit.probation_revoked && probation_revoked_date !== "") {
    edit["probation_revoked"] = probation_revoked_date;
  }
  return edit;
}


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
        loading: "",
      };
    case RECORD_LOADING:
      return {...state, record: {}, aliases: JSON.parse(JSON.stringify(action.aliases)), questions: {}, edits: {}, loading: "loading"};
    case CLEAR_RECORD:
      return {...state, record: {}, aliases: [], questions: {}, edits: {}, loading: ""};
    case SELECT_ANSWER: {
      let questions: QuestionsData = JSON.parse(JSON.stringify(state.questions));
      if (questions && questions[action.ambiguous_charge_id]) {
        const question = findQuestion(questions[action.ambiguous_charge_id].root, action.question_id);
        if (question) {
          clearSelection(question);
          question.selection = action.answer;
          if (action.date !== "") {
            replaceDispositionDate(question, action.date);
          }
          if (action.probation_revoked_date !== "") {
            replaceProbationRevokedDate(question, action.probation_revoked_date);
          }
        }
      }
      const edit = replaceDatesInEdit(JSON.parse(JSON.stringify(action.edit)), action.date, action.probation_revoked_date);
      const edits = JSON.parse(JSON.stringify(state.edits));
      edits[action.case_number] = edits[action.case_number] || {"action": "edit"};
      edits[action.case_number]["charges"] = edits[action.case_number]["charges"] || {};
      edits[action.case_number]["charges"][action.ambiguous_charge_id] = edits[action.case_number]["charges"][action.ambiguous_charge_id] || {};
      edits[action.case_number]["charges"][action.ambiguous_charge_id] = edit;
      return {...state, questions: questions, edits: edits, loading: action.ambiguous_charge_id};
    }
    default:
      return state;
  }
}
