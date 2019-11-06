import axios, { AxiosPromise } from 'axios';

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

const REQUEST = 'REQUEST';

export default function apiService(
  dispatch: Function,
  request: Request
): AxiosPromise {
  dispatch({ type: REQUEST, request });
  return axios.request(request);
}
