import { DateTime } from "luxon";
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

export const initialState: SearchFormState = {
  aliases: [
    {
      first_name: "",
      middle_name: "",
      last_name: "",
      birth_date: "",
    },
  ],
  date: DateTime.now().toFormat("M/d/yyyy"),
};

interface UpdateAliasPayload {
  index: number;
  attribute: AliasFieldNames;
  value: string;
}

export const searchFormSlice = createSlice({
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
} = searchFormSlice.actions;

export const selectSearchFormValues = (state: RootState) => ({
  aliases: state.searchForm.aliases,
  date: state.searchForm.date,
});

export default searchFormSlice.reducer;
