import 'bootstrap/dist/css/bootstrap.css';

import React, { Suspense } from 'react';
import Page from './Page.js'
import './App.css';
import { AuthenticationProvider } from './authentication/AuthenticationContext.js';
import { BrowserRouter as Router } from 'react-router-dom';
import { SightingProvider } from './sighting/SightingContext.js';
import SuspenseLoader from './suspense/SuspenseLoader';

export default () => {

  return (
    <Router>
      <AuthenticationProvider>
        <SightingProvider>
          <Suspense fallback={<SuspenseLoader />}>
            <Page />
          </Suspense>
        </SightingProvider>
      </AuthenticationProvider>
    </Router>
  );
}
