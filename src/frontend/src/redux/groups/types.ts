import { User } from '../users/types'

export interface GroupState {
  groupList: Group[];
}

export interface Group {
  id: number;
  name: string;
  users: User[];
}

export const LOAD_GROUPS = 'LOAD_GROUPS';

interface LoadGroupsAction {
  type: typeof LOAD_GROUPS;
  groups: Group[];
}

export type GroupActionTypes = LoadGroupsAction;
