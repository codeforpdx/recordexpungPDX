import { createSelector } from "reselect";
import { CaseData } from "../../components/RecordSearch/Record/types";
import { AppState } from "../store";

const getRecordState = (state: AppState) => state.search.record;

export const hasBalanceDue = (element: CaseData) => {
  return element.balance_due > 0;
};

export const selectCasesWithBalanceDue = createSelector(
  [getRecordState],
  (record) => {
    return record?.cases?.filter(hasBalanceDue) ?? [];
  }
);
