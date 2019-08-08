import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Suspense } from 'react';
import Page from './Page.js'
import './App.css';

function App() {

  const Loader = () => (
    <div className="App">
      <div>loading...</div>
    </div>
  );

  return (
    <Suspense fallback={<Loader />}>
      <Page />
    </Suspense>
  );
}

export default App;
