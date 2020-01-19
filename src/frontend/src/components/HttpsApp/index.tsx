import React from 'react';
import HttpsRedirect from '../../service/https-redirect';
import App from '../App';

class HttpsApp extends React.Component {
  render() {
    return (
      <HttpsRedirect>
        <App />
      </HttpsRedirect>
    );
  }
}

export default HttpsApp;
