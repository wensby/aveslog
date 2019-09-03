import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Suspense } from 'react';
import Page from './Page.js'
import './App.css';
import { AuthenticationProvider } from './authentication/AuthenticationContext.js';
import { BrowserRouter as Router } from 'react-router-dom';

export default () => {

  const Loader = () => (
    <div className="App">
      <div>loading...</div>
    </div>
  );

  return (
    <Router>
      <AuthenticationProvider>
        <Suspense fallback={<Loader />}>
          <Page />
        </Suspense>
      </AuthenticationProvider>
    </Router>
  );
}
