// See the following guides for an explanation:
// https://redux-starter-kit.js.org/usage/usage-guide
// https://redux.js.org/recipes/usage-with-typescript
import { configureStore, getDefaultMiddleware } from '@reduxjs/toolkit';
import { combineReducers } from 'redux';

// Reducers:
import { usersReducer } from './users/reducer';
import { searchReducer } from './search/reducer';
import { systemReducer } from './system/reducer';
import { groupsReducer } from './groups/reducer';

const rootReducer = combineReducers({
  system: systemReducer,
  search: searchReducer,
  users: usersReducer,
  groups: groupsReducer
});

const store = configureStore({
  reducer: rootReducer,
  middleware: [...getDefaultMiddleware()]
});

export type AppState = ReturnType<typeof rootReducer>;

export default store;
