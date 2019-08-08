import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Navbar from './navbar/navbar.js';
import SideMenu from './sidemenu.js';
import Login from './Login.js'
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
        <Link className="nav-link" to={`/profile/${this.state.username}`}>{t('Profile')}</Link>,
        <Link className="nav-link" to={'/sighting/'}>{t('Sightings')}</Link>,
        <Link className="nav-link" to={'/settings/'}>{t('Settings')}</Link>,
        <Link className="nav-link" to={'/authentication/logout'}>{t('Logout')}</Link>
      ];
    } else {
      return [
        <Link className="nav-link" to={'/settings/'}>{t('Settings')}</Link>,
        <Link className="nav-link" to={'/authentication/login'}>{t('Login')}</Link>
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