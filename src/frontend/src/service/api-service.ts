import axios, { AxiosPromise, AxiosRequestConfig } from 'axios';
import { removeCookie } from './cookie-service';
import { LOG_OUT } from '../redux/system/types';

export default function apiService(
  dispatch: Function,
  request: AxiosRequestConfig
): AxiosPromise {
  return axios.request(request).catch(error => {
    if (error.response && error.response.status === 401) {
      removeCookie();
      dispatch({ type: LOG_OUT });
    }
    return Promise.reject(error);
  });
}
