import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Navbar from './navbar/navbar.js';
import SideMenu from './sidemenu.js';
import Login from './authentication.js'
import Settings from './settings/settings'
import Home from './home/home.js';
import './App.css';
import { withTranslation } from 'react-i18next';

class Page extends Component {

  constructor(props) {
    super(props);
    this.state = {};
  };

  getMenuItems = () => {
    const { t } = this.props;
    if (localStorage.getItem('authToken')) {
      return [
        { href: `/profile/${this.state.username}`, text: t('Profile') },
        { href: '/sighting/', text: t('Sightings') },
        { href: '/authentication/logout', text: t('Logout') },
        { href: '/settings/', text: t('Settings') }
      ];
    } else {
      return [
        { href: '/authentication/login', text: t('Login') },
        { href: '/settings/', text: t('Settings') }
      ];
    }
  }

  render() {
    const menuItems = this.getMenuItems();

    return (
      <Router>
        <Navbar items={menuItems} />
        <div className='main-grid navbar-pushed'>
          <SideMenu items={menuItems} />
          <main role="main" className="col-12 col-md-9 col-lg-8">
            <Route path='/' exact component={Home} />
            <Route path="/authentication/login" exact component={Login} />
            <Route path='/settings/' exact component={Settings} />
          </main>
        </div>
      </Router>
    );
  }
}

export default withTranslation()(Page);