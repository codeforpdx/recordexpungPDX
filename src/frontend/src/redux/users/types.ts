export interface UserState {
  userList: User[];
  addUser?: boolean;
  editID: number;
  editName: string;
  editEmail: string;
  editGroup: string;
  editAdmin: boolean;
}

export interface User {
  admin: boolean;
  email: string;
  group: string;
  id: number;
  name: string;
  timestamp: Date;
}

export const LOAD_USERS = 'LOAD_USERS';
export const CLEAR_USERS = 'CLEAR_USERS';
export const ADD_USER = 'ADD_USER';
export const EDIT_USER = 'EDIT_USER';
export const EDIT_USER_POPULATE = 'EDIT_USER_POPULATE';

interface LoadUsersAction {
  type: typeof LOAD_USERS;
  users: User[];
  addUser: boolean;
}
interface AddUserAction {
  type: typeof ADD_USER;
  addUser: boolean;
}
interface EditUserAction {
  type: typeof EDIT_USER;
  addUser: boolean;
}
interface ToEditUserAction {
  type: typeof EDIT_USER_POPULATE;
  addUser: boolean;
  editID: number;
  editName: string;
  editEmail: string;
  editGroup: string;
  editAdmin: boolean;
}
interface ClearUserAction {
  type: typeof CLEAR_USERS;
  users: User[];
}

export type UserActionTypes = LoadUsersAction | ClearUserAction | AddUserAction | ToEditUserAction | EditUserAction;
