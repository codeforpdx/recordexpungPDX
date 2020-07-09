import {
  RecordData,
  RecordSummaryData,
  QuestionsData,
} from "../../components/RecordSearch/Record/types";
import { AliasData } from "../../components/RecordSearch/SearchPanel/types";

export interface SearchResponse {
  record: RecordEndpointData;
}

export interface RecordEndpointData {
  total_balance_due: number;
  cases: any[];
  errors: string[];
  summary: RecordSummaryData;
  questions: QuestionsData;
}

export const DISPLAY_RECORD = "DISPLAY_RECORD";
export const RECORD_LOADING = "RECORD_LOADING";
export const CLEAR_RECORD = "CLEAR_RECORD";
export const SELECT_ANSWER = "SELECT_ANSWER";
export const LOADING_PDF = "LOADING_PDF";
export const LOADING_PDF_COMPLETE = "LOADING_PDF_COMPLETE";
export const EDIT_CASE = "EDIT_CASE";
export const DELETE_CASE = "DELETE_CASE";
export const UNDO_EDIT_CASE = "UNDO_EDIT_CASE";
export const EDIT_CHARGE = "EDIT_CHARGE";
export const DELETE_CHARGE = "DELETE_CHARGE";
export const UNDO_EDIT_CHARGE = "UNDO_EDIT_CHARGE";
export const START_EDITING = "START_EDITING";
export const DONE_EDITING = "DONE_EDITING";

export interface SearchRecordState {
  loading: string;
  loadingPdf: boolean;
  aliases: AliasData[];
  record?: RecordData;
  questions?: QuestionsData;
  edits?: any;
  editingRecord: boolean;
}

interface SearchRecordAction {
  type:
    | typeof DISPLAY_RECORD
    | typeof RECORD_LOADING
    | typeof CLEAR_RECORD
    | typeof LOADING_PDF
    | typeof LOADING_PDF_COMPLETE;
  aliases: AliasData[];
  record: RecordData;
  questions: QuestionsData;
}

export interface QuestionsAction {
  type: typeof SELECT_ANSWER;
  ambiguous_charge_id: string;
  case_number: string;
  question_id: string;
  answer: string;
  edit: any;
  date: string;
  probation_revoked_date: string;
}

interface EditCaseAction {
  type: typeof EDIT_CASE;
  edit_status: string;
  case_number: string;
  status: string;
  county: string;
  balance: string;
  birth_year: string;
}

interface DeleteCaseAction {
  type: typeof DELETE_CASE;
  case_number: string;
}

interface UndoEditCaseAction {
  type: typeof UNDO_EDIT_CASE;
  case_number: string;
}

interface EditChargeAction {
  type: typeof EDIT_CHARGE;
  edit_status: string;
  case_number: string;
  ambiguous_charge_id: string;
  charge_date: string;
  ruling: string;
  disposition_date: string;
  probation_revoked_date: string;
  charge_type: string;
  charge_name: string;
}

interface DeleteChargeAction {
  type: typeof DELETE_CHARGE;
  case_number: string;
  ambiguous_charge_id: string;
}

interface UndoEditChargeAction {
  type: typeof UNDO_EDIT_CHARGE;
  case_number: string;
  ambiguous_charge_id: string;
}

interface StartEditingAction {
  type: typeof START_EDITING;
}

interface DoneEditingAction {
  type: typeof DONE_EDITING;
}

export type SearchRecordActionType =
  | SearchRecordAction
  | QuestionsAction
  | EditCaseAction
  | DeleteCaseAction
  | UndoEditCaseAction
  | EditChargeAction
  | DeleteChargeAction
  | UndoEditChargeAction
  | StartEditingAction
  | DoneEditingAction;
