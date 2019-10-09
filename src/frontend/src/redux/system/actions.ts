import apiService from '../../service/api-service';
import { setCookie, removeCookie } from '../../service/cookie-service';
import history from '../../service/history';
import { LOG_IN, LOG_OUT } from './types';

export function logIn(email: string, password: string): any {
  return (dispatch: Function) => {
    return apiService(dispatch, {
      url: '/api/auth_token',
      data: { email, password },
      method: 'post'
    }).then((response: any) => {
      dispatch({
        type: LOG_IN,
        userId: response.data.user_id,
        authToken: response.data.auth_token
      });
      setCookie(response.data.auth_token, response.data.user_id);
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

export function refreshLocalAuth(inputToken: string, inputId: string) {
  // refresh the 'max-age' for cookie while user is active
  setCookie(inputToken, inputId);
  return {
    type: LOG_IN,
    userId: inputId,
    authToken: inputToken
  };
}
