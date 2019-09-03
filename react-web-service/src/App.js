import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Suspense } from 'react';
import Page from './Page.js'
import './App.css';
import { AuthenticationProvider } from './authentication/AuthenticationContext.js';

export default () => {

  const Loader = () => (
    <div className="App">
      <div>loading...</div>
    </div>
  );

  return (
    <AuthenticationProvider>
      <Suspense fallback={<Loader />}>
        <Page />
      </Suspense>
    </AuthenticationProvider>
  );
}
