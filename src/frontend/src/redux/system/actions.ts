import { LOG_IN, LOG_OUT, LogInData } from './types';

export function logIn(data: LogInData) {
  return {
    type: LOG_IN,
    userId: data.user_id,
    authToken: data.auth_token
  };
}

export function logOut() {
  return {
    type: LOG_OUT,
    authToken: ''
  };
}
