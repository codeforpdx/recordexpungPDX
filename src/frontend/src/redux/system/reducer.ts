import { LOG_IN, LOG_OUT, SystemState, SystemActionTypes } from './types';

const initialState: SystemState = {
  loggedIn: false,
  userId: '',
  authToken: ''
};

export function systemReducer(
  state = initialState,
  action: SystemActionTypes
): SystemState {
  switch (action.type) {
    case LOG_IN: {
      return {
        loggedIn: true,
        userId: action.userId,
        authToken: action.authToken
      };
    }
    case LOG_OUT: {
      return {
        loggedIn: false,
        userId: '',
        authToken: ''
      };
    }
    default:
      return state;
  }
}
