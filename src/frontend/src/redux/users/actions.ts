import { Dispatch } from 'redux';
import { LOAD_USERS } from './types';
import apiService from '../../service/api-service';

export const loadUsers = () => {
  return (dispatch: Dispatch) => {
    return apiService(dispatch, {
      url: '/api/users',
      method: 'get'
    }).then((response: any) => {
      dispatch({
        type: LOAD_USERS,
        users: response.data.users
      });
    });
  };
};
