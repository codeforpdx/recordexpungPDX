import apiService from '../../service/api-service';
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
      history.push('/oeci');
    });
  };
}

export function logOut() {
  return {
    type: LOG_OUT,
    authToken: ''
  };
}
