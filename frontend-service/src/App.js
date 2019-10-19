import 'bootstrap/dist/css/bootstrap.css';

import React, { Suspense } from 'react';
import Page from './Page.js'
import { AuthenticationProvider } from './authentication/AuthenticationContext.js';
import { BrowserRouter as Router } from 'react-router-dom';
import { SightingProvider } from './sighting/SightingContext.js';
import SuspenseLoader from './suspense/SuspenseLoader';

export default ({ version }) => {
  prepareLocalStorage(version);

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

/**
 * Clears the local storage and updates the app version if the version differs
 * from previously set app version.
 */
function prepareLocalStorage(version) {
  const key = 'appVersion';
  const storedVersion = localStorage.getItem(key);
  if (!storedVersion || storedVersion !== version) {
    localStorage.clear();
    localStorage.setItem(key, version);
  }
}
