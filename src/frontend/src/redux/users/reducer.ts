import { CLEAR_USERS, LOAD_USERS, UserActionTypes, UserState } from './types';

const initialState: UserState = {
  userList: []
};

export function usersReducer(
  state = initialState,
  action: UserActionTypes
): UserState {
  switch (action.type) {
    case LOAD_USERS:
      return {
        userList: action.users
      };
    case CLEAR_USERS:
      return {
        userList: []
      };
    default:
      return state;
  }
}
