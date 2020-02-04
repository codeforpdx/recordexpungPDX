import { LOG_IN, LOG_OUT, SystemState, SystemActionTypes } from './types';

const initialState: SystemState = {
  loggedIn: false,
  isAdmin: false
};

export function systemReducer(
  state = initialState,
  action: SystemActionTypes
): SystemState {
  switch (action.type) {
    case LOG_IN: {
      return {
        loggedIn: true,
        isAdmin: action.isAdmin
      };
    }
    case LOG_OUT: {
      return {
        loggedIn: false
      };
    }
    default:
      return state;
  }
}
