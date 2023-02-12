import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "./store";
import { RECORD_LOADING, DISPLAY_RECORD } from "./search/types";
interface EditingState {
  isEditing: boolean;
}

const initialState: EditingState = {
  isEditing: false,
};

function resetState() {
  return initialState;
}

export const editingSlice = createSlice({
  name: "editing",
  initialState,
  reducers: {
    startEditing: (state) => {
      state.isEditing = true;
    },
    doneEditing: resetState,
  },
  extraReducers: (builder) => {
    builder.addCase(RECORD_LOADING, resetState);
    builder.addCase(DISPLAY_RECORD, resetState);
  },
});

export const { startEditing, doneEditing } = editingSlice.actions;

export const selectIsEditing = (state: RootState) => state.editing.isEditing;

export default editingSlice.reducer;
