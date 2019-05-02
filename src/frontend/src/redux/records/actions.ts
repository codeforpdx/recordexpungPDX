import { Record, LOAD_RECORDS } from "./types";

// This function is an action creator.
export function loadRecords(records: Record[]) {
  // Values returned here are actions.
  return {
    type: LOAD_RECORDS,
    records
  };
}
