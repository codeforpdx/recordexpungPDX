export interface UserState {
  userList: User[];
}

export interface User {
  email: string;
  group: string;
  id: number;
  name: string;
  role: string;
}

export const LOAD_USERS = 'LOAD_USERS';

interface LoadUsersAction {
  type: typeof LOAD_USERS;
  users: User[];
}

export type UserActionTypes = LoadUsersAction;
