import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "./store";
import {
  AliasData,
  AliasFieldNames,
} from "../components/RecordSearch/SearchPanel/types";

interface SearchFormState {
  date: string;
  aliases: AliasData[];
}

const initialState: SearchFormState = {
  aliases: [
    {
      first_name: "",
      middle_name: "",
      last_name: "",
      birth_date: "",
    },
  ],
  date: "",
};

interface UpdateAliasPayload {
  index: number;
  attribute: AliasFieldNames;
  value: string;
}

export const formSlice = createSlice({
  name: "searchForm",
  initialState,
  reducers: {
    setSearchFormDate: (state, action) => {
      state.date = action.payload;
    },
    updateSearchFormAlias: (state, action) => {
      const { index, attribute, value } = action.payload as UpdateAliasPayload;
      state.aliases[index][attribute] = value;
    },
    addSearchFormAlias: (state) => {
      state.aliases.push({ ...state.aliases[state.aliases.length - 1] });
    },
    removeSearchFormAlias: (state, action) => {
      state.aliases.splice(action.payload.index, 1);
    },
  },
});

export const {
  setSearchFormDate,
  updateSearchFormAlias,
  addSearchFormAlias,
  removeSearchFormAlias,
} = formSlice.actions;

export const selectSearchFormAliases = (state: RootState) =>
  state.searchForm.aliases;

export const selectSearchFormDate = (state: RootState) => state.searchForm.date;

export default formSlice.reducer;
