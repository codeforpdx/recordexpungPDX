import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RootState } from "./store";
import {
  RecordData,
  ShortLabel,
} from "../components/RecordSearch/Record/types";

type StatusCountMap = {
  [key in ShortLabel]?: {
    total: number;
    numIncluded: number;
    numExcluded: number;
  };
};

type FinesCountyMap = { [key: string]: number };

interface StatsState {
  totalCases: number;
  totalCharges: number;
  numExcludedCharges: number;
  numIncludedCharges: number;
  totalFines: number;
  numChargesByEligibilityStatus: StatusCountMap;
  finesByCounty: FinesCountyMap;
}

const initialState: StatsState = {
  totalCases: 0,
  totalCharges: 0,
  numExcludedCharges: 0,
  numIncludedCharges: 0,
  totalFines: 0,
  numChargesByEligibilityStatus: {},
  finesByCounty: {},
};

function getStatsFromCharges(record: RecordData) {
  const statusStats: StatusCountMap = {};
  const cases = record.cases;
  let numExcludedCharges = 0;

  if (!cases) return { numExcludedCharges, statusStats };

  cases.forEach((aCase) => {
    aCase.charges.forEach(({ shortLabel, isExcluded }) => {
      if (isExcluded) numExcludedCharges++;

      if (!shortLabel) return;

      if (!statusStats[shortLabel]) {
        statusStats[shortLabel] = {
          total: 0,
          numIncluded: 0,
          numExcluded: 0,
        };
      }

      statusStats[shortLabel]!.total++;
      isExcluded
        ? statusStats[shortLabel]!.numExcluded++
        : statusStats[shortLabel]!.numIncluded++;
    });
  });

  return { numExcludedCharges, statusStats };
}

function getFinesByCounty(record: RecordData) {
  const finesByCounty: FinesCountyMap = {};
  const summary = record.summary;

  if (!summary) return finesByCounty;

  return summary.county_fines.reduce(
    (fines, { county_name, total_fines_due }) => {
      fines[county_name] = total_fines_due;
      return fines;
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
        return action.payload;
      },
      prepare(record: RecordData) {
        let stats = initialState;
        let summary = record.summary;

        if (!summary) return { payload: stats };

        stats = {
          totalCases: summary.total_cases,
          totalCharges: summary.total_charges,
          numExcludedCharges: 0,
          numIncludedCharges: 0,
          totalFines: summary.total_fines_due,
          numChargesByEligibilityStatus: {},
          finesByCounty: {},
        };

        const { numExcludedCharges, statusStats } = getStatsFromCharges(record);
        stats.numExcludedCharges = numExcludedCharges;
        stats.numIncludedCharges = stats.totalCharges - numExcludedCharges;
        stats.numChargesByEligibilityStatus = statusStats;
        stats.finesByCounty = getFinesByCounty(record);

        return { payload: stats };
      },
    },
  },
});

export const { updateStats } = statsSlice.actions;

export const selectStats = (state: RootState) => state.stats;

export default statsSlice.reducer;
