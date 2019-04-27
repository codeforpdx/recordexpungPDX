// See the following guides for an explanation:
// https://redux-starter-kit.js.org/usage/usage-guide
// https://redux.js.org/recipes/usage-with-typescript
import { configureStore } from 'redux-starter-kit'
import { combineReducers } from "redux";

// Reducers:
import { recordsReducer } from './records/reducers';

const store = configureStore({
  reducer: combineReducers({ records: recordsReducer }),
})

export default store;
