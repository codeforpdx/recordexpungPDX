import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "./store";

interface EditingState {
  isEditing: boolean;
}

const initialState: EditingState = {
  isEditing: false,
};

export const editingSlice = createSlice({
  name: "editing",
  initialState,
  reducers: {
    startEditing: (state) => {
      state.isEditing = true;
    },
    doneEditing: (state) => {
      state.isEditing = false;
    },
  },
});

export const { startEditing, doneEditing } = editingSlice.actions;

export const selectIsEditing = (state: RootState) => state.editing.isEditing;

export default editingSlice.reducer;
