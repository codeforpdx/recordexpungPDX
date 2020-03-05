// See the following guides for an explanation:
// https://redux-starter-kit.js.org/usage/usage-guide
// https://redux.js.org/recipes/usage-with-typescript
import { configureStore, getDefaultMiddleware } from '@reduxjs/toolkit';
import { combineReducers } from 'redux';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

// Reducers:
import { usersReducer } from './users/reducer';
import { recordsReducer } from './records/reducer';
import { systemReducer } from './system/reducer';
import { groupsReducer } from './groups/reducer';

const persistConfig = {
  key: 'root',
  storage,
  version: 1,
  whitelist: ['system']
};

const systemConfig = {
  key: 'system',
  storage,
  whitelist: ['isAdmin']
};

const rootReducer = combineReducers({
  system: persistReducer(systemConfig, systemReducer),
  records: recordsReducer,
  users: usersReducer,
  groups: groupsReducer
});

const pReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
  reducer: pReducer,
  middleware: getDefaultMiddleware({
    serializableCheck: false
  })
});

export const persistor = persistStore(store);

export type AppState = ReturnType<typeof rootReducer>;

export default store;
