import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Suspense } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Navbar from './navbar/navbar.js';
import SideMenu from './sidemenu.js';
import Login from './authentication.js'
import Settings from './settings/settings'
import './App.css';
import { useTranslation } from "react-i18next";

function Page() {
  const { t } = useTranslation();

  const menuItems = [{
    href: '/authentication/login',
    text: t('Login')
  },
  {
    href: '/settings/',
    text: t('Settings')
  }];

  return (
    <Router>
      <Navbar items={menuItems}/>
      <div className='main-grid navbar-pushed'>
        <SideMenu items={menuItems} />
        <main role="main" className="col-12 col-md-9 col-lg-8">
          <Route path="/authentication/login" exact component={Login} />
          <Route path='/settings/' exact component={Settings} />
        </main>
      </div>
    </Router>
  );
}

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
