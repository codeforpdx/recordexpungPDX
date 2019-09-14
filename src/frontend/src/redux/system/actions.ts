import axios from 'axios';
import { LOG_IN, LOG_OUT } from './types';

export function logIn(token: string) {
  axios.defaults.headers.common = { Authorization: `Bearer ${token}` };
  return {
    type: LOG_IN
  };
}

export function logOut() {
  delete axios.defaults.headers.common['Authorization'];
  return {
    type: LOG_OUT
  };
}
