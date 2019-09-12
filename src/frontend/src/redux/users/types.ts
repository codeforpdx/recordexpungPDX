export interface UserState {
  userList: UserTypes[];
}

export interface UserTypes {
  email: string;
  group: string;
  id: number;
  name: string;
  role: string;
}

export const LOAD_USERS = 'LOAD_USERS';

interface LoadUsersAction {
  type: typeof LOAD_USERS;
  users: UserTypes[];
}

export type UserActionTypes = LoadUsersAction;
