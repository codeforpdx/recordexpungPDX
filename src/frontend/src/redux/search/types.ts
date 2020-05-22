import {
  RecordData,
  RecordSummaryData,
  QuestionsData
} from '../../components/RecordSearch/Record/types'
import {AliasData} from "../../components/RecordSearch/SearchPanel/types";

export interface SearchResponse {
  record: RecordEndpointData;
}

export interface RecordEndpointData {
  total_balance_due: number;
  cases: any[];
  errors: string[];
  summary: RecordSummaryData;
  questions: QuestionsData;
  disposition_was_unknown: string[];
}

export const DISPLAY_RECORD = 'DISPLAY_RECORD';
export const RECORD_LOADING = 'RECORD_LOADING';
export const CLEAR_RECORD = 'CLEAR_RECORD';
export const SELECT_ANSWER = 'SELECT_ANSWER';
export const ANSWER_DISPOSITION = 'ANSWER_DISPOSITION';
export const EDIT_CASE = 'EDIT_CASE';
export const DELETE_CASE = 'DELETE_CASE';
export const UNDO_EDIT_CASE = 'UNDO_EDIT_CASE';

export interface SearchRecordState {
  loading: boolean;
  aliases: AliasData[];
  record?: RecordData;
  questions?: QuestionsData;
  edits?: any;
  dispositionWasUnknown: string[];
  nextNewCaseNum: number
}

interface SearchRecordAction {
  type:
    | typeof DISPLAY_RECORD
    | typeof RECORD_LOADING
    | typeof CLEAR_RECORD;
  aliases: AliasData[];
  record: RecordData;
  questions: QuestionsData;
  dispositionWasUnknown: string[];
}

interface QuestionsAction {
  ambiguous_charge_id: string;
  type: typeof SELECT_ANSWER;
  answer: string;
}

interface AnswerDispositionAction {
  type: typeof ANSWER_DISPOSITION;
  case_number: string;
  ambiguous_charge_id: string;
  probation_revoked_edit: string;
  disposition_edit: any; // TODO: Properly type
}

interface EditCaseAction {
  type: typeof EDIT_CASE;
  edit_type: string,
  case_number: string,
  status: string,
  county: string,
  balance_due: string,
  birth_year: string
}

interface DeleteCaseAction {
  type: typeof DELETE_CASE;
  case_number: string,
}

interface UndoEditCaseAction {
  type: typeof UNDO_EDIT_CASE;
  case_number: string,
}
export type SearchRecordActionType = SearchRecordAction | QuestionsAction | AnswerDispositionAction | EditCaseAction | DeleteCaseAction | UndoEditCaseAction;
