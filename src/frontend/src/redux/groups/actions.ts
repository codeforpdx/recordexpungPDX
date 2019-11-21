import { Dispatch } from 'redux';
import { LOAD_GROUPS, Group } from './types';

export const loadGroups = () => (dispatch: Dispatch) => {
  return new Promise(resolve => {
    setTimeout(() => {
      // placeholderGroupData will be replaced with the payload from the axios request
      const groups: Group[] = placeholderGroupData;
      resolve(
        dispatch({
          type: LOAD_GROUPS,
          groups
        })
      )

    }, 1000);
  });
};

// Data for loadGroups action to populate the store with group data
const placeholderGroupData: Group[] = [
  {
    id: 1,
    name: 'Metropolitan Public Defender',
    users: [
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
      }
    ]
  },
  {
    id: 1,
    name: 'Chicken and Cow LLC',
    users: [
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
    ]
  },
  {
    id: 1,
    name: 'Dolphin and whale inc',
    users: [
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
    ]
  },
  {
    id: 1,
    name: 'Royce, Jennings & Coldwater',
    users: [
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
      }
    ]
  }

];
