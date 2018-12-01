import * as React from 'react';
import * as ReactDOM from 'react-dom';
import App from './components/app/App';
import './main.style.scss';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(
  <App />,
  document.getElementById('root') as HTMLElement
);
registerServiceWorker();
