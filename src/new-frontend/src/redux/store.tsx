// See https://redux-starter-kit.js.org/usage/usage-guide
import { configureStore } from 'redux-starter-kit'
import rootReducer from './reducers/index';

const store = configureStore({
  reducer: rootReducer
})

export default store;
