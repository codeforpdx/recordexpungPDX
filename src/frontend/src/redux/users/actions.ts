import { Dispatch } from 'redux';
import { LOAD_USERS, CLEAR_USERS, ADD_USER } from './types';
import apiService from '../../service/api-service';
import history from '../../service/history';

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

export const addUser = (name: string, email: string, password: string, group_name: string, admin: boolean) => {
  return (dispatch: Dispatch) => {
    return apiService(dispatch, {
      url: '/api/users',
      data: { name, email, password, group_name, admin },
      method: 'post',
    }).then((response: any) => {
      console.log(response);
      dispatch({
        type: ADD_USER,
      });
      history.push('/admin');
    });
  };
};

export const clearUsers = () => {
  return (dispatch: Dispatch) => {
    dispatch({
      type: CLEAR_USERS
    });
  };
};
