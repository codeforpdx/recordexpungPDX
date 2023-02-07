import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RootState } from "./store";
import {
  RecordData,
  ChargeEligibilityStatus,
} from "../components/RecordSearch/Record/types";

interface StatsState {
  totalCases: number;
  totalCharges: number;
  totalFines: number;
  numChargesByEligibilityStatus?: Map<ChargeEligibilityStatus, number>;
  finesByCounty?: Map<string, number>;
}

const initialState: StatsState = {
  totalCases: 0,
  totalCharges: 0,
  totalFines: 0,
};

// TODO: when data is loading in actions.storeSearchResponse()
// create a new status of "Eligible" which is use for "Eligible Now" but with
// conditions like when fines are due
function getStatusStatsFromCharges(record: RecordData) {
  const statusStats = new Map<ChargeEligibilityStatus, number>();
  const cases = record.cases;

  if (!cases) return statusStats;

  return cases.reduce((stats, aCase) => {
    aCase.charges.forEach(
      ({
        expungement_result: {
          charge_eligibility: { status },
        },
      }) => {
        stats.set(status, (stats.get(status) ?? 0) + 1);
      }
    );
    return statusStats;
  }, statusStats);
}

function getFinesByCounty(record: RecordData) {
  const finesByCounty = new Map<string, number>();
  const summary = record.summary;

  if (!summary) return finesByCounty;

  return summary.county_fines.reduce(
    (fines, { county_name, total_fines_due }) => {
      return fines.set(county_name, total_fines_due);
    },
    finesByCounty
  );
}

export const statsSlice = createSlice({
  name: "stats",
  initialState,
  reducers: {
    updateStats: {
      reducer(state, action: PayloadAction<StatsState>) {
        state = action.payload;
      },
      prepare(record: RecordData) {
        let stats = initialState;
        let summary = record.summary;

        if (!summary) return { payload: stats };

        stats = {
          totalCases: summary.total_cases,
          totalCharges: summary.total_charges,
          totalFines: summary.total_fines_due,
        };

        stats.numChargesByEligibilityStatus = getStatusStatsFromCharges(record);
        stats.finesByCounty = getFinesByCounty(record);

        return { payload: stats };
      },
    },
  },
});

export const { updateStats } = statsSlice.actions;

export const selectStats = (state: RootState) => state.stats;

export default statsSlice.reducer;
