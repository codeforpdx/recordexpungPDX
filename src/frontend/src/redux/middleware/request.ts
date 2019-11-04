import { Request } from '../../service/api-service';
import axios, { AxiosPromise } from 'axios';
import { Action, Dispatch, MiddlewareAPI } from 'redux';
import { logOut } from '../system/actions';

// This Redux Action type shouldn't be used outside of here and service/api-service.ts
export const REQUEST = 'REQUEST';

// This Action and Middleware is a sort of implementation detail of the API Service needed
// to allow API Requests to interact with the application state via the Redux store.
export interface RequestAction {
  type: typeof REQUEST;
  request: Request;
}

// This is a custom Middleware that does three things:
// - Actually calls axios to make requests created with apiService
// - Adds the Authorization header to requests where request.authenticated is true
// - Check that we're actually logged in before making an 'authenticated' request
//
// The goal of this Middleware is to handle request authentication with all state managed
// in the Store, and without extra work from application code. apiService now requires the
// dispatch function as a first argument, but because apiService still returns a promise,
// this is a relatively flexible approach that doesn't require you to put *all* state in the
// Store. For a similar but different approach (with more state in the Store) see
// https://auth0.com/blog/secure-your-react-and-redux-app-with-jwt-authentication/
//
// If, for example, someone decides to add persistent sessions (you stay logged in even if
// you refresh the page) this Middleware makes it easier to do so. Note that storing a JWT
// in the Store or in Local Storage is vulnerable to XSS.
//
// Can't figure out the types here for the moment. Help is welcome!
const RequestMiddleware = (store: MiddlewareAPI) => (next: Dispatch) => (
  anyAction: Action
) => {
  if (anyAction.type !== REQUEST) {
    return next(anyAction);
  }

  const action = anyAction as RequestAction;

  // Make the request normally if it doesn't need or expect authentication.
  if (
    !(action.request.authenticated && action.request.authenticated === true)
  ) {
    let promise = makeUnauthenticatedRequest(action);
    let result = next(action);
    return Object.assign({ promise }, result);
  }

  // This error shouldn't occur because app code has access to the store and thus knows
  // whether or not we're currently authenticated. This error shouldn't be handled by
  // rejecting the Promise returned by apiService since this is an error in our code, not
  // a failure with the request.
  throwUnlessCurrentlyAuthenticated(store);

  let promise = makeAuthenticatedRequest(store, action);
  let result = next(action);
  return Object.assign({ promise }, result);
};

function makeUnauthenticatedRequest(action: RequestAction): AxiosPromise {
  return axios.request(action.request);
}

function makeAuthenticatedRequest(
  store: MiddlewareAPI,
  action: RequestAction
): AxiosPromise {
  return axios
    .request(withAuthorizationHeader(store, action).request)
    .catch(error => {
      if (
        error.response &&
        error.response.status &&
        error.response.status === 401 &&
        !error.response.data.includes('Invalid OECI username or password.')
      ) {
        store.dispatch(logOut());
      }
      return Promise.reject(error);
    });
}

function throwUnlessCurrentlyAuthenticated(store: MiddlewareAPI): void {
  const message =
    'Attempted to make an authenticated request without actually being authenticated';

  const token = getAuthToken(store);
  if (token && token.length > 0) {
    return;
  }

  alert("There's a bug. Please notify the developers: " + message);
  throw message;
}

function withAuthorizationHeader(store: MiddlewareAPI, action: RequestAction) {
  return Object.assign({}, action, {
    request: Object.assign({}, action.request, {
      headers: Object.assign({}, action.request.headers, {
        Authorization: 'Bearer ' + getAuthToken(store)
      })
    })
  });
}

function getAuthToken(store: MiddlewareAPI) {
  return store.getState().system.authToken;
}

export default RequestMiddleware;
