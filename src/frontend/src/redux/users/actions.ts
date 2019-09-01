import { User, LOAD_USERS } from './types';

export const loadUsers = (users: User[]) => (dispatch: Function) => {
  dispatch({
    type: LOAD_USERS,
    users
  });
};
