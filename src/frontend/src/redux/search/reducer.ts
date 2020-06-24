import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  CLEAR_RECORD,
  SELECT_ANSWER,
  EDIT_CASE,
  DELETE_CASE,
  EDIT_CHARGE,
  DELETE_CHARGE,
  UNDO_EDIT_CASE,
  UNDO_EDIT_CHARGE,
  SearchRecordState,
  SearchRecordActionType,
} from "./types";
import {
  QuestionData,
  QuestionsData,
} from "../../components/RecordSearch/Record/types";

const initalState: SearchRecordState = {
  loading: "",
  aliases: [],
  edits: {},
};

function findQuestion(
  question: QuestionData,
  question_id: string
): null | QuestionData {
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

function replaceProbationRevokedDate(
  question: QuestionData,
  probation_revoked_date: string
) {
  for (const answer of Object.values(question.options)) {
    if (answer.edit && answer.edit.probation_revoked) {
      answer.edit["probation_revoked"] = probation_revoked_date;
    }
    if (answer.question) {
      replaceProbationRevokedDate(answer.question, probation_revoked_date);
    }
  }
}

function replaceDatesInEdit(
  edit: any,
  date: string,
  probation_revoked_date: string
) {
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
      return {
        ...state,
        record: {},
        aliases: JSON.parse(JSON.stringify(action.aliases)),
        questions: {},
        edits: {},
        loading: "loading",
      };
    case CLEAR_RECORD:
      return {
        ...state,
        record: {},
        aliases: [],
        questions: {},
        edits: {},
        loading: "",
      };
    case SELECT_ANSWER: {
      let questions: QuestionsData = JSON.parse(
        JSON.stringify(state.questions)
      );
      if (questions && questions[action.ambiguous_charge_id]) {
        const question = findQuestion(
          questions[action.ambiguous_charge_id].root,
          action.question_id
        );
        if (question) {
          clearSelection(question);
          question.selection = action.answer;
          if (action.date !== "") {
            replaceDispositionDate(question, action.date);
          }
          if (action.probation_revoked_date !== "") {
            replaceProbationRevokedDate(
              question,
              action.probation_revoked_date
            );
          }
        }
      }
      const edit = replaceDatesInEdit(
        JSON.parse(JSON.stringify(action.edit)),
        action.date,
        action.probation_revoked_date
      );
      const edits = JSON.parse(JSON.stringify(state.edits));
      edits[action.case_number] = edits[action.case_number] || {
        summary: { edit_status: "UPDATE" },
      };
      edits[action.case_number]["charges"] =
        edits[action.case_number]["charges"] || {};
      edits[action.case_number]["charges"][action.ambiguous_charge_id] = edit;
      return {
        ...state,
        questions: questions,
        edits: edits,
        loading: action.ambiguous_charge_id,
      };
    }

    case EDIT_CASE: {
      const edits = JSON.parse(JSON.stringify(state.edits));
      if (!edits[action.case_number]) {
        edits[action.case_number] = {};
      } // This check lets edits merge and not overwrite each other (e.g. AnswerDisposition vs EditCase)
      edits[action.case_number]["summary"] = {
        case_number: action.case_number,
        current_status: action.status,
        location: action.county,
        balance_due: action.balance,
        birth_year: action.birth_year,
        edit_status: action.edit_status,
      };
      return {
        ...state,
        edits: edits,
        loading: "edit",
      };
    }

    case DELETE_CASE: {
      const edits = JSON.parse(JSON.stringify(state.edits));
      edits[action.case_number] = { summary: { edit_status: "DELETE" } };
      return { ...state, edits: edits, loading: "edit" };
    }

    case UNDO_EDIT_CASE: {
      const edits = JSON.parse(JSON.stringify(state.edits));
      const filtered_edits = Object.keys(edits)
        .filter((key) => action.case_number !== key)
        .reduce((res: any, key) => ((res[key] = edits[key]), res), {});
      return { ...state, edits: filtered_edits };
    }

    case EDIT_CHARGE: {
      const edits = JSON.parse(JSON.stringify(state.edits));
      if (!edits[action.case_number]) {
        edits[action.case_number] = {
          summary: { edit_status: "UPDATE" },
        };
      }
      if (!edits[action.case_number]["charges"]) {
        edits[action.case_number]["charges"] = {};
      }
      edits[action.case_number]["charges"][action.ambiguous_charge_id] = {
        edit_status: action.edit_status,
        date: action.charge_date,
        disposition: {
          ruling: action.ruling,
          date: action.disposition_date,
        },
        probation_revoked: action.probation_revoked_date,
        charge_type: action.charge_type,
        name: action.charge_name,
      };
      return {
        ...state,
        edits: edits,
        loading: "edit",
      };
    }

    case DELETE_CHARGE: {
      const edits = JSON.parse(JSON.stringify(state.edits));
      if (!edits[action.case_number]) {
        edits[action.case_number] = { summary: { edit_status: "UPDATE" } };
      } // This check lets edits merge and not overwrite each other (e.g. AnswerDisposition vs EditCase)
      //edits[action.case_number]["summary"]["edit_status"] = "UPDATE";
      if (!edits[action.case_number]["charges"]) {
        edits[action.case_number]["charges"] = {};
      }
      edits[action.case_number]["charges"][action.ambiguous_charge_id] = {
        edit_status: "DELETE",
      };
      return { ...state, edits: edits };
    }

    case UNDO_EDIT_CHARGE: {
      {
        let edits = JSON.parse(JSON.stringify(state.edits));
        if (edits[action.case_number]["summary"]["edit_status"] == "DELETE") {
          const ambiguous_charge_ids_on_case =
            state && state.record && state.record.cases
              ? state.record.cases
                  .filter(
                    (caseData) => caseData.case_number === action.case_number
                  )[0]
                  ["charges"].map(
                    (caseData: any) => caseData.ambiguous_charge_id
                  )
              : [];
          if (ambiguous_charge_ids_on_case.length === 1) {
            /*Undo only deleted charge on case means undo the deleted case.*/
            edits = Object.keys(edits)
              .filter((key) => action.case_number !== key)
              .reduce((res: any, key) => ((res[key] = edits[key]), res), {});
            return { ...state, edits: edits };
          } else {
            /*Undo deleted charge on a deleted case that has other charges means
          we must mark the other charges as deleted.*/
            const delete_charge_edits = ambiguous_charge_ids_on_case
              .filter((val: string) => val !== action.ambiguous_charge_id)
              .reduce(
                (res: any, key: string) => (
                  (res[key] = { edit_status: "DELETE" }), res
                ),
                {}
              );
            edits[action.case_number]["summary"]["edit_status"] = "UPDATE";
            edits[action.case_number]["charges"] = delete_charge_edits;
            return { ...state, edits: edits };
          }
        } else {
          /* The case edit status is "ADD" or "UPDATE" */
          /* This charge update gets filtered out; otherwise the edit on that case
        is unchanged. */

          /* Todo: if the case status is UPDATE,
          and the undo reverts the last charge edit,
          and there are no other updates to the case summary, then remove the case edit entry entirely.*/
          if (
            Object.keys(edits[action.case_number]["summary"]).length === 1 &&
            Object.keys(edits[action.case_number]["charges"]).length === 1
          ) {
            edits = Object.keys(edits)
              .filter((key) => action.case_number !== key)
              .reduce((res: any, key) => ((res[key] = edits[key]), res), {});
            return { ...state, edits: edits };
          }

          /* otherwise just remove the charge edit and leave the rest intact.*/
          const filtered_charge_edits = Object.keys(
            edits[action.case_number]["charges"]
          )
            .filter((key) => key !== action.ambiguous_charge_id)
            .reduce(
              (res: any, key) => (
                (res[key] = edits[action.case_number]["charges"][key]), res
              ),
              {}
            );
          //edits[action.case_number] ["summary"]["edit_status"] = "UPDATE";
          edits[action.case_number]["charges"] = filtered_charge_edits;
          return { ...state, edits: edits };
        }
      }
    }
    default:
      return state;
  }
}
