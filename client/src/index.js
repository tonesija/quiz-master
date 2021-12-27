import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Auth0Provider from './auth0-provider';

ReactDOM.render(
  <React.StrictMode>
    <Auth0Provider>
      <App/>
    </Auth0Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

