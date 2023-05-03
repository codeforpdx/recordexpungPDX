import { createSlice } from '@reduxjs/toolkit';
import { hasOeciToken } from '../service/cookie-service';

const initialState = {
  loggedIn: hasOeciToken(),
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setLoggedIn: (state, action) => {
      state.loggedIn = action.payload;
    },
  },
});

export const { setLoggedIn } = authSlice.actions;

export default authSlice.reducer;
