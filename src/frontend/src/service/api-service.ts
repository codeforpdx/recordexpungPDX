import axios, { AxiosPromise, AxiosRequestConfig } from 'axios';
import { removeCookie } from './cookie-service';
import { LOG_OUT } from '../redux/system/types';

export default function apiService<T>(
  dispatch: Function,
  request: AxiosRequestConfig
): AxiosPromise {
  return axios.request<T>(request).catch(error => {
    if (error.response && error.response.status === 401 && error.response.message === "Invalid username or password") {
      // This logs the app out if any endpoint request is denied app authorization
      // The exact string comparison ensures that it catches only the errors thrown by
      // app authorization, and not from an OECI login failure which also has a 401 code.
      removeCookie();
      dispatch({ type: LOG_OUT });
    }
    return Promise.reject(error);
  });
}
