import { CLEAR_USERS, LOAD_USERS, ADD_USER, UserActionTypes, UserState } from './types';

const initialState: UserState = {
  userList: [],
  addUser: false
};

export function usersReducer(
  state = initialState,
  action: UserActionTypes
): UserState {
  switch (action.type) {
    case LOAD_USERS:
      return {
        userList: action.users,
        addUser: false
      };
    case ADD_USER:
      return {
        userList: [],
        addUser: true
      };
    case CLEAR_USERS:
      return {
        userList: [],
        addUser: false
      };
    default:
      return state;
  }
}
