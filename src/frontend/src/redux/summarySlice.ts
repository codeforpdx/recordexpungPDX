import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "./store";

interface SummaryState {
  isLoading: boolean;
}

const initialState: SummaryState = {
  isLoading: false,
};

export const summarySlice = createSlice({
  name: "summary",
  initialState,
  reducers: {
    startLoadingSummary: (state) => {
      state.isLoading = true;
    },
    stopLoadingSummary: (state) => {
      state.isLoading = false;
    },
  },
});

export const { startLoadingSummary, stopLoadingSummary } = summarySlice.actions;

export const selectSummaryIsLoading = (state: RootState) =>
  state.summary.isLoading;

export default summarySlice.reducer;
