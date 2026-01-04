import {
  DISPLAY_RECORD,
  RECORD_LOADING,
  SELECT_ANSWER,
  EDIT_CASE,
  DELETE_CASE,
  EDIT_CHARGE,
  DELETE_CHARGE,
  UNDO_EDIT_CASE,
  UNDO_EDIT_CHARGE,
  DOWNLOAD_EXPUNGEMENT_PACKET,
  LOADING_EXPUNGEMENT_PACKET_COMPLETE,
  SearchRecordState,
  SearchRecordActionType,
  DOWNLOAD_WAIVER_PACKET,
  LOADING_WAIVER_PACKET_COMPLETE,
  DISMISS_ALL_RESTITUTION,
} from "./types";
import {
  QuestionData,
  QuestionsData,
} from "../../components/RecordSearch/Record/types";
import initialState from "./initialState";

function findQuestion(
  question: QuestionData,
  question_id: string
): null | QuestionData {
  if (question.question_id === question_id) {
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

function clearAnswersForCaseOrCharge(
  questions_state_data: any,
  case_number: string,
  ambiguous_charge_id: string
) {
  let questions: QuestionsData = JSON.parse(
    JSON.stringify(questions_state_data)
  );

  if (questions) {
    Object.keys(questions).forEach((key: string) => {
      if (case_number === questions[key].case_number) {
        clearSelection(questions[key].root);
      }
      if (ambiguous_charge_id === questions[key].ambiguous_charge_id) {
        clearSelection(questions[key].root);
      }
    });
  }
  return questions;
}

export function searchReducer(
  state = initialState,
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
        questions: {},
        edits: {},
        loading: "loading",
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
        summary: { edit_status: "UNCHANGED" },
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
      edits[action.case_number] = edits[action.case_number] || {};
      edits[action.case_number]["summary"] = {
        case_number: action.case_number,
        current_status: action.status,
        restitution: action.restitution,
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
      return {
        ...state,
        edits: edits,
        questions: clearAnswersForCaseOrCharge(
          state.questions,
          action.case_number,
          ""
        ),
        loading: "edit",
      };
    }

    case UNDO_EDIT_CASE: {
      const edits = JSON.parse(JSON.stringify(state.edits));
      const editsFromQuestions =
        edits[action.case_number]["charges"] &&
        Object.entries(edits[action.case_number]["charges"])
          .filter((entry: [string, any]) => !entry[1]["edit_status"])
          .reduce((res: any, entry) => {
            res[entry[0]] = entry[1];
            return res;
          }, {});

      const filtered_edits = Object.keys(edits)
        .filter((key) => action.case_number !== key)
        .reduce((res: any, key) => {
          res[key] = edits[key];
          return res;
        }, {});
      if (editsFromQuestions && Object.keys(editsFromQuestions).length > 0) {
        filtered_edits[action.case_number] = {
          summary: { edit_status: "UNCHANGED" },
          charges: editsFromQuestions,
        };
      }

      return { ...state, edits: filtered_edits };
    }

    case DISMISS_ALL_RESTITUTION: {
      const edits = JSON.parse(JSON.stringify(state.edits));
      action.cases
        .filter((c) => c.restitution === true)
        .forEach((c) => {
          edits[c.case_number] = edits[c.case_number] || {};
          edits[c.case_number]["summary"] = {
            ...edits[c.case_number]["summary"],
            case_number: c.case_number,
            current_status: c.current_status,
            restitution: "False",
            location: c.location,
            balance_due: String(c.balance_due),
            birth_year: c.birth_year ? String(c.birth_year) : "",
            edit_status: edits[c.case_number]?.summary?.edit_status || "UPDATE",
          };
        });
      return {
        ...state,
        edits: edits,
        loading: "edit",
      };
    }

    case EDIT_CHARGE: {
      const edits = JSON.parse(JSON.stringify(state.edits));

      if (!edits[action.case_number]) {
        edits[action.case_number] = {
          summary: { edit_status: "UPDATE" },
        };
      }
      edits[action.case_number]["charges"] =
        edits[action.case_number]["charges"] || {};

      edits[action.case_number]["charges"][action.ambiguous_charge_id] = {
        edit_status: action.edit_status,
        date: action.charge_date,
        disposition: {
          ruling: action.ruling,
          date: action.disposition_date,
        },
        probation_revoked: action.probation_revoked_date,
        charge_type: action.charge_type,
        level: action.level,
        name: action.charge_name,
      };
      return {
        ...state,
        edits: edits,
        questions: clearAnswersForCaseOrCharge(
          state.questions,
          "",
          action.ambiguous_charge_id
        ),
        loading: "edit",
      };
    }

    case DELETE_CHARGE: {
      const edits = JSON.parse(JSON.stringify(state.edits));
      edits[action.case_number] = edits[action.case_number] || {
        summary: { edit_status: "UPDATE" },
      };
      edits[action.case_number]["charges"] =
        edits[action.case_number]["charges"] || {};
      edits[action.case_number]["charges"][action.ambiguous_charge_id] = {
        edit_status: "DELETE",
      };
      return {
        ...state,
        edits: edits,
        questions: clearAnswersForCaseOrCharge(
          state.questions,
          action.case_number,
          ""
        ),
        loading: "edit",
      };
    }

    case UNDO_EDIT_CHARGE: {
      let edits = JSON.parse(JSON.stringify(state.edits));
      if (edits[action.case_number]["summary"]["edit_status"] === "DELETE") {
        const ambiguous_charge_ids_on_case =
          state && state.record && state.record.cases
            ? state.record.cases
                .filter(
                  (caseData) => caseData.case_number === action.case_number
                )[0]
                ["charges"].map((caseData: any) => caseData.ambiguous_charge_id)
            : [];
        if (ambiguous_charge_ids_on_case.length === 1) {
          /*Undoing the only deleted charge on a deleted case means undo the entire delete action on the case.*/
          edits = Object.keys(edits)
            .filter((key) => action.case_number !== key)
            .reduce((res: any, key) => {
              res[key] = edits[key];
              return res;
            }, {});
        } else {
          /*If the case was deleted, but we are undoing the delete on one charge,
            and the case has other charges, they should remain deleted. That means we
            now mark the case as "updated" and we need to explicitly mark the other charges as deleted.
            */
          const delete_charge_edits = ambiguous_charge_ids_on_case
            .filter((val: string) => val !== action.ambiguous_charge_id)
            .reduce((res: any, key: string) => {
              res[key] = { edit_status: "DELETE" };
              return res;
            }, {});
          edits[action.case_number]["summary"]["edit_status"] = "UPDATE";
          edits[action.case_number]["charges"] = delete_charge_edits;
        }
      } else {
        /* The case edit status is "ADD" or "UPDATE" */
        /* This charge update gets filtered out; otherwise the edit on that case
        is unchanged. */

        /* If the case status is UPDATE, and the undo reverts the last charge edit,
          and there are no other updates to the case summary, then remove the case edit entry entirely.*/
        if (
          Object.keys(edits[action.case_number]["summary"]).length === 1 &&
          Object.keys(edits[action.case_number]["charges"]).length === 1
        ) {
          edits = Object.keys(edits)
            .filter((key) => action.case_number !== key)
            .reduce((res: any, key) => {
              res[key] = edits[key];
              return res;
            }, {});
        } else {
          /* otherwise just remove the charge edit and leave the rest intact.*/
          const filtered_charge_edits = Object.keys(
            edits[action.case_number]["charges"]
          )
            .filter((key) => key !== action.ambiguous_charge_id)
            .reduce((res: any, key) => {
              res[key] = edits[action.case_number]["charges"][key];
              return res;
            }, {});
          edits[action.case_number]["charges"] = filtered_charge_edits;
        }
      }
      return { ...state, edits };
    }
    case DOWNLOAD_EXPUNGEMENT_PACKET:
      const information = {
        full_name: action.name,
        date_of_birth: action.dob,
        mailing_address: action.mailingAddress,
        phone_number: action.phoneNumber,
        city: action.city,
        state: action.state,
        zip_code: action.zipCode,
        email_address: action.emailAddress,
      };
      return {
        ...state,
        userInformation: information,
        loadingExpungementPacket: true,
      };
    case LOADING_EXPUNGEMENT_PACKET_COMPLETE:
      return {
        ...state,
        loadingExpungementPacket: false,
      };
    case DOWNLOAD_WAIVER_PACKET:
      const userInformation = {
        full_name: action.name,
        date_of_birth: action.dob,
        mailing_address: action.mailingAddress,
        phone_number: action.phoneNumber,
        city: action.city,
        state: action.state,
        zip_code: action.zipCode,
      };
      const waiverInformation = {
        explain: action.explain,
        explain2: action.explain2,
        snap: action.snap,
        ssi: action.ssi,
        tanf: action.tanf,
        ohp: action.ohp,
        custody: action.custody,
      };
      return {
        ...state,
        userInformation,
        waiverInformation,
        loadingWaiverPacket: true,
      };
    case LOADING_WAIVER_PACKET_COMPLETE:
      return {
        ...state,
        loadingWaiverPacket: false,
      };
    default:
      return state;
  }
}
