import { CLEAR_USERS, LOAD_USERS, ADD_USER, EDIT_USER, EDIT_USER_POPULATE, UserActionTypes, UserState } from './types';

const initialState: UserState = {
  userList: [],
  addUser: false,
  editID: 0,
  editName: '',
  editEmail: '',
  editGroup: '',
  editAdmin: false,
};

export function usersReducer(
  state = initialState,
  action: UserActionTypes
): UserState {
  switch (action.type) {
    case LOAD_USERS:
      return {
        ...state,
        userList: action.users,
        addUser: false
      };
    case ADD_USER:
      return {
        ...state,
        userList: [],
        addUser: true
      };
    case EDIT_USER:
      return {
        ...state,
        addUser: false,
      };
    case EDIT_USER_POPULATE:
      return {
        ...state,
        userList: [],
        addUser: false,
        editID: action.editID,
        editName: action.editName,
        editEmail: action.editEmail,
        editGroup: action.editGroup,
        editAdmin: action.editAdmin,
      };
    case CLEAR_USERS:
      return {
        ...state,
        userList: [],
        addUser: false
      };
    default:
      return state;
  }
}
