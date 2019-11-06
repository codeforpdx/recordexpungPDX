import apiService from '../../service/api-service';
import { removeCookie, hasOeciToken } from '../../service/cookie-service';
import history from '../../service/history';
import { LOG_IN, LOG_OUT } from './types';
import { Dispatch } from 'redux';

export function logIn(email: string, password: string): any {
  return (dispatch: Dispatch) => {
    return apiService(dispatch, {
      url: '/api/auth_token',
      data: { email, password },
      method: 'post'
    }).then((response: any) => {
      dispatch({
        type: LOG_IN
      });
      history.push('/oeci');
    });
  };
}

export function logOut() {
  removeCookie();
  return {
    type: LOG_OUT
  };
}

export function refreshLocalAuth() {
  return {
    type: LOG_IN
  };
}

export function oeciLogIn(username: string, password: string): any {
  return (dispatch: Dispatch) => {
    return apiService(dispatch, {
      url: '/api/oeci_login',
      data: { oeci_username: username, oeci_password: password },
      method: 'post',
      authenticated: true,
      withCredentials: true
    }).then((response: any) => {
      if (hasOeciToken()) {
        history.push('/record-search');
      }
    });
  };
}
