// See the following guides for an explanation:
// https://redux-starter-kit.js.org/usage/usage-guide
// https://redux.js.org/recipes/usage-with-typescript
import { configureStore, getDefaultMiddleware } from 'redux-starter-kit';
import { combineReducers } from 'redux';
import RequestMiddleware from './middleware/request';

// Reducers:
import { usersReducer } from './users/reducer';
import { recordsReducer } from './records/reducer';
import { systemReducer } from './system/reducer';

const rootReducer = combineReducers({
  system: systemReducer,
  records: recordsReducer,
  users: usersReducer
});

const store = configureStore({
  reducer: rootReducer,
  middleware: [...getDefaultMiddleware(), RequestMiddleware]
});

export type AppState = ReturnType<typeof rootReducer>;

export default store;
