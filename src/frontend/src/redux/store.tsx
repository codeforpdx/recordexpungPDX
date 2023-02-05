// https://redux-starter-kit.js.org/usage/usage-guide
// https://redux.js.org/recipes/usage-with-typescript

import { configureStore, PreloadedState } from "@reduxjs/toolkit";
import { combineReducers } from "redux";
import { searchReducer } from "./search/reducer";

const rootReducer = combineReducers({
  search: searchReducer,
});

const store = configureStore({
  reducer: rootReducer,
});

export const setupStore = (preloadedState?: PreloadedState<RootState>) => {
  return configureStore({
    reducer: rootReducer,
    preloadedState,
  });
};

export type AppState = ReturnType<typeof rootReducer>;
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export type AppStore = ReturnType<typeof setupStore>;

export default store;
