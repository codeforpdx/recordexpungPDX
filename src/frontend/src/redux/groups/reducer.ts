import { LOAD_GROUPS, GroupActionTypes, GroupState } from './types';

const initialState: GroupState = {
  groupList: []
};

export function groupsReducer(
  state = initialState,
  action: GroupActionTypes
): GroupState {
  switch (action.type) {
    case LOAD_GROUPS:
      return {
        groupList: action.groups
      };
    default:
      return state;
  }
}
