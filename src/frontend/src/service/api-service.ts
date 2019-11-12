import axios, { AxiosPromise } from 'axios';
import { logOut } from '../redux/system/actions';

type Method = 'post' | 'delete' | 'get' | 'head' | 'delete' | 'options' | 'put';

// If 'authenticated' is true then the RequestMiddleware will add
// our authentication token (a JWT) as the authorization header for
// the request.
export type Request = {
  url: string;
  data?: object;
  method: Method;
  headers?: object;
  authenticated?: boolean;
  withCredentials?: boolean;
};

export default function apiService(
  dispatch: Function,
  request: Request
): AxiosPromise {
  return axios.request(request).catch(error => {
    if (error.response && error.response.status === 401) {
      dispatch(logOut());
    }
    return Promise.reject(error);
  });
}
