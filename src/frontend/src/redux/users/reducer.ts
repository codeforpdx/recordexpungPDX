import { UserState, UserActionTypes, LOAD_USERS } from './types';

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
    default:
      return state;
  }
}
