import { REQUEST, RequestAction } from '../redux/middleware/request';
import { AxiosPromise } from 'axios';

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

// The dispatch function is needed in order to send requests to the Request Middleware, which
// handles authentication.
export default function apiService(
  dispatch: Function,
  request: Request
): AxiosPromise {
  // The Action dispatched here is handled in the Request Middleware, so you can call
  // apiService(...).then(...).catch(...) like a normal Axios request.
  let result = dispatch({ type: REQUEST, request } as RequestAction);
  return result.promise;
}
