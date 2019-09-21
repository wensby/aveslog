import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Suspense } from 'react';
import Page from './Page.js'
import './App.css';
import { AuthenticationProvider } from './authentication/AuthenticationContext.js';
import { BrowserRouter as Router } from 'react-router-dom';
import Loading from './Loading';

export default () => {

  return (
    <Router>
      <AuthenticationProvider>
        <Suspense fallback={<Loading />}>
          <Page />
        </Suspense>
      </AuthenticationProvider>
    </Router>
  );
}
