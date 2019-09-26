export interface SystemState {
  loggedIn: boolean;
  userId: string;
  authToken: string;
}

export const LOG_IN = 'LOG_IN';
export const LOG_OUT = 'LOG_OUT';

interface LogInAction {
  type: typeof LOG_IN;
  userId: string;
  authToken: string;
}

interface LogOutAction {
  type: typeof LOG_OUT;
  authToken: string;
}

export type SystemActionTypes = LogInAction | LogOutAction;
