import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "./store";

interface DemoState {
  isOn: boolean;
}

const initialState: DemoState = {
  isOn: false,
};

export const demoSlice = createSlice({
  name: "demo",
  initialState,
  reducers: {
    startDemo: (state) => {
      state.isOn = true;
    },
    stopDemo: (state) => {
      state.isOn = false;
    },
  },
});

export const { startDemo, stopDemo } = demoSlice.actions;

export const selectDemoStatus = (state: RootState) => state.demo.isOn;

export default demoSlice.reducer;
