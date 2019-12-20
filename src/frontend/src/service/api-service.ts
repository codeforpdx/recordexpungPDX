import axios, { AxiosPromise, AxiosRequestConfig } from 'axios';
import { removeCookie } from './cookie-service';
import { LOG_OUT } from '../redux/system/types';

export default function apiService<T>(
  dispatch: Function,
  request: AxiosRequestConfig
): AxiosPromise {
  return axios.request<T>(request).catch(error => {
    if (error.response && error.response.status === 401 && error.response.message === "Invalid username or password") {
      // To avoid catching the 401 error due to an OECI login failure
      removeCookie();
      dispatch({ type: LOG_OUT });
    }
    return Promise.reject(error);
  });
}
