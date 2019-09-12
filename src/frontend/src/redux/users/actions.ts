import { Dispatch } from 'redux';
import { LOAD_USERS, User } from './types';

export const loadUsers = () => (dispatch: Dispatch) => {
  return new Promise(resolve => {
    setTimeout(() => {
      // placeholderUserData will be replaced with the payload from the axios request
      const users: User[] = placeholderUserData;
      dispatch({
        type: LOAD_USERS,
        users
      });
    }, 1000);
  });
};

// Data for loadUsers action to populate the store with user data
const placeholderUserData: User[] = [
  {
    email: 'jane@email.com',
    group: 'Metropolitan Public Defender',
    id: 1,
    name: 'Jane Dolby',
    role: 'Search'
  },
  {
    email: 'michael@email.com',
    group: 'Metropolitan Public Defender',
    id: 2,
    name: 'Michael Zhang',
    role: 'Admin'
  },
  {
    email: 'melissa@email.com',
    group: 'Royce, Jennings & Coldwater',
    id: 3,
    name: 'Melissa Jennings',
    role: 'Search'
  },
  {
    email: 'terri@email.com',
    group: 'Royce, Jennings & Coldwater',
    id: 4,
    name: 'Terri Royce',
    role: 'Search'
  }
];
