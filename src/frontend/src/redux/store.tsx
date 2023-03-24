// https://redux-starter-kit.js.org/usage/usage-guide
// https://redux.js.org/recipes/usage-with-typescript

import { configureStore, PreloadedState, createAction } from "@reduxjs/toolkit";
import { combineReducers, AnyAction } from "redux";
import { searchReducer } from "./search/reducer";
import demoReducer from "./demoSlice";
import summarySlice from "./summarySlice";
import editingSlice from "./editingSlice";
import statsSlice from "./statsSlice";
import searchFormSlice from "./searchFormSlice";
import authSlice from "./authSlice";

export const clearAllData = createAction("CLEAR_ALL_DATA");

const appReducer = combineReducers({
  search: searchReducer,
  demo: demoReducer,
  summary: summarySlice,
  editing: editingSlice,
  stats: statsSlice,
  searchForm: searchFormSlice,
  auth: authSlice,
});

// https://stackoverflow.com/questions/35622588/how-to-reset-the-state-of-a-redux-store
const rootReducer: typeof appReducer = (
  state: AppState | undefined,
  action: AnyAction
) => {
  return action.type === clearAllData.type
    ? appReducer(undefined, action)
    : appReducer(state, action);
};

const store = configureStore({
  reducer: rootReducer,
});

export const setupStore = (preloadedState?: PreloadedState<RootState>) => {
  return configureStore({
    reducer: rootReducer,
    preloadedState,
  });
};

export type AppState = ReturnType<typeof appReducer>;
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export type AppStore = ReturnType<typeof setupStore>;

export default store;
