// See the following guides for an explanation:
// https://redux-starter-kit.js.org/usage/usage-guide
// https://redux.js.org/recipes/usage-with-typescript
import { configureStore } from 'redux-starter-kit';
import { combineReducers } from 'redux';

// Reducers:

import { systemReducer } from './system/reducer';
import { searchRecordsReducer } from './records/reducer';

const rootReducer = combineReducers({
  system: systemReducer,

  searchRecordsReducer
});

const store = configureStore({ reducer: rootReducer });

export type AppState = ReturnType<typeof rootReducer>;

export default store;
