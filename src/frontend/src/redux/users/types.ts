export interface UserState {
  userList: User[];
}

export interface User {
  name: string;
  role: string;
  group: string;
}

export const LOAD_USERS = 'LOAD_USERS';

interface LoadUsersAction {
  type: typeof LOAD_USERS;
  users: User[];
}

export type UserActionTypes = LoadUsersAction;
