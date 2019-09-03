import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React from 'react';
import { Route } from "react-router-dom";
import Navbar from './navbar/navbar.js';
import SideMenu from './sidemenu.js';
import Settings from './settings/settings'
import Home from './home/Home.js';
import './App.css';
import Authentication from './authentication/Authentication.js'
import Bird from './bird/Bird.js';
import Sighting from './sighting/Sighting.js';

export default () => {
  return (
    <>
      <Navbar />
      <div className='main-grid navbar-pushed'>
        <SideMenu />
        <main role="main">
          <Route path='/' exact component={Home} />
          <Route path='/authentication' component={Authentication} />
          <Route path='/settings/' exact component={Settings} />
          <Route path='/bird' component={Bird} />
          <Route path='/sighting' component={Sighting} />
        </main>
      </div>
    </>
  );
}
