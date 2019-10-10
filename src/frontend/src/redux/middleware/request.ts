import { Request } from '../../service/api-service';
import axios from 'axios';
import { Store, Action } from 'redux';
import { logOut } from '../system/actions';

// This Redux Action type shouldn't be used outside of here and service/api-service.ts
export const REQUEST = 'REQUEST';

// This Action and Middleware is a sort of implementation detail of the API Service needed
// to allow API Requests to interact with the application state via the Redux store.
export interface RequestAction {
  type: typeof REQUEST;
  request: Request;
  resolve: Function;
  reject: Function;
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
const RequestMiddleware: any = (store: Store) => (next: Function) => (
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
    makeUnauthenticatedRequest(action);
    return next(withoutUnserializables(action));
  }

  // This error shouldn't occur because app code has access to the store and thus knows
  // whether or not we're currently authenticated. This error shouldn't be handled by
  // rejecting the Promise returned by apiService since this is an error in our code, not
  // a failure with the request.
  throwUnlessCurrentlyAuthenticated(store);

  makeAuthenticatedRequest(store, action);
  return next(withoutUnserializables(action));
};

function makeUnauthenticatedRequest(action: RequestAction): void {
  axios
    .request(action.request)
    .then(action.resolve as any, action.reject as any);
}

// Make the request with Axios and when the Promise Axios returns resolves or rejects,
// send the control flow back to the Promise returned by apiService.
function makeAuthenticatedRequest(store: Store, action: RequestAction): void {
  // Can't figure out the types here for the moment. Help is welcome!
  axios
    .request(withAuthorizationHeader(store, action).request)
    .then(action.resolve as any, error => {
      if (
        error.response &&
        error.response.status &&
        error.response.status === 401
      ) {
        store.dispatch(logOut());
      }
      action.reject(error);
    });
}

function throwUnlessCurrentlyAuthenticated(store: Store): void {
  const message =
    'Attempted to make an authenticated request without actually being authenticated';

  const token = getAuthToken(store);
  if (token && token.length > 0) {
    return;
  }

  alert("There's a bug. Please notify the developers: " + message);
  throw message;
}

function withAuthorizationHeader(store: Store, action: RequestAction) {
  return Object.assign({}, action, {
    request: Object.assign({}, action.request, {
      headers: Object.assign({}, action.request.headers, {
        Authorization: 'Bearer ' + getAuthToken(store)
      })
    })
  });
}

// Redux Starter Kit includes the serializable-state-invariant-middleware which logs a
// warning message in development if an Action is dispatched containing non-serializable
// data, including functions like RequestAction.resolve. The goal of this is to guide
// folks to avoid putting non-serializable data in the Store. Since we aren't doing that
// here, this Middleware can safely work around this check by omitting the Functions in
// RequestAction before passing the Action on to other Middleware. The only "gotcha" here
// is that this Middleware needs to be first in line to avoid the error message-- which is
// handled in frontend/src/redux/store.tsx.
//
// See https://redux.js.org/faq/actions#why-should-type-be-a-string-or-at-least-serializable-why-should-my-action-types-be-constants
// for more info.
function withoutUnserializables(action: RequestAction) {
  return { type: action.type, request: action.request };
}

function getAuthToken(store: Store) {
  return store.getState().system.authToken;
}

export default RequestMiddleware;
