export interface SystemState {
  loggedIn: boolean;
}

export const LOG_IN = 'LOG_IN';
export const LOG_OUT = 'LOG_OUT';

interface LogInAction {
  type: typeof LOG_IN;
}

interface LogOutAction {
  type: typeof LOG_OUT;
}

export type SystemActionTypes = LogInAction | LogOutAction;
