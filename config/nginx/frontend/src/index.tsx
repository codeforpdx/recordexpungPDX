// These imports are all defaults from create-react-app.
import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import * as serviceWorker from './serviceWorker';
import './index.scss';

// The following is based on the example code at
// https://react-redux.js.org/introduction/quick-start
import { Provider } from 'react-redux';
import store from './redux/store';

const rootElement = document.getElementById('root');
ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  rootElement
);

// Service Workers are intentionally turned off; they were causing
// issues when testing URLs.

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
