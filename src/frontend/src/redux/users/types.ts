export interface UserState {
  userList: User[];
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

interface LoadUsersAction {
  type: typeof LOAD_USERS;
  users: User[];
}

interface ClearUserAction {
  type: typeof CLEAR_USERS;
  users: User[];
}

export type UserActionTypes = LoadUsersAction | ClearUserAction;
