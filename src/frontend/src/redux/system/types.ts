export interface SystemState {
  loggedIn: boolean;
  isAdmin?: boolean;
}

export const LOG_IN = 'LOG_IN';
export const LOG_OUT = 'LOG_OUT';

interface LogInAction {
  type: typeof LOG_IN;
  loggedIn: boolean;
  isAdmin: boolean;
}

interface LogOutAction {
  type: typeof LOG_OUT;
  loggedIn: boolean;
}

export type SystemActionTypes = LogInAction | LogOutAction;
