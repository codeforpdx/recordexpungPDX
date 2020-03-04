export interface UserState {
  userList: User[];
  addUser?: boolean;
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
export const ADD_USER ="ADD_USER";

interface LoadUsersAction {
  type: typeof LOAD_USERS;
  users: User[];
  addUser: boolean;
}
interface AddUserAction {
  type: typeof ADD_USER;
  addUser: boolean;
}

interface ClearUserAction {
  type: typeof CLEAR_USERS;
  users: User[];
}

export type UserActionTypes = LoadUsersAction | ClearUserAction | AddUserAction;
