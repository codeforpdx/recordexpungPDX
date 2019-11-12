import axios, { AxiosPromise } from 'axios';
import { removeCookie } from './cookie-service';
import { LOG_OUT } from '../redux/system/types';

type Method = 'post' | 'delete' | 'get' | 'head' | 'delete' | 'options' | 'put';

// If 'authenticated' is true then the RequestMiddleware will add
// our authentication token (a JWT) as the authorization header for
// the request.
export type Request = {
  url: string;
  data?: object;
  method: Method;
  headers?: object;
  withCredentials?: boolean;
};

export default function apiService(
  dispatch: Function,
  request: Request
): AxiosPromise {
  return axios.request(request).catch(error => {
    if (error.response && error.response.status === 401) {
      removeCookie();
      dispatch({ type: LOG_OUT });
    }
    return Promise.reject(error);
  });
}
