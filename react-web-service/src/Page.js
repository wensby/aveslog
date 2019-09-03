import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Component } from 'react';
import { Route } from "react-router-dom";
import Navbar from './navbar/navbar.js';
import SideMenu from './sidemenu.js';
import Settings from './settings/settings'
import Home from './home/HomePage.js';
import './App.css';
import { withTranslation } from 'react-i18next';
import Authentication from './authentication/Authentication.js'
import Bird from './bird/Bird.js';
import Sighting from './sighting/Sighting.js';

class Page extends Component {

  constructor(props) {
    super(props);
  };

  render() {
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
}

export default withTranslation()(Page);
