import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Component } from 'react';
import { Route, Link } from "react-router-dom";
import Navbar from './navbar/navbar.js';
import SideMenu from './sidemenu.js';
import Settings from './settings/settings'
import Home from './home/home.js';
import './App.css';
import { withTranslation } from 'react-i18next';
import AuthenticationService from './authentication/AuthenticationService.js';
import Authentication from './authentication/Authentication.js'
import AccountService from './account/AccountService';
import Bird from './bird/Bird.js';
import Sighting from './sighting/Sighting.js';

class Page extends Component {

  constructor(props) {
    super(props);
    this.state = {
      authenticated: false,
      account: null,
    };
  };

  setAuthenticated = async () => {
    const account = await (new AccountService().get_account(localStorage.getItem('authToken')));
    this.setState({
      authenticated: true,
      account: account
    });
  }

  onLogout = async () => {
    await (new AuthenticationService().logout());
    this.setState({ authenticated: false });
  }

  getMenuItems = () => {
    const { t } = this.props;
    const { authenticated, account } = this.state;

    if (authenticated) {
      return [
        <Link className="nav-link"
            to={`/profile/${account.username}`}>{t('Profile')}</Link>,
        <Link className="nav-link"
            to={'/sighting'}>{t('Sightings')}</Link>,
        <Link className="nav-link"
            to={'/settings/'}>{t('Settings')}</Link>,
        <Link className="nav-link" onClick={this.onLogout}
            to={'/authentication/logout'}>{t('Logout')}</Link>
      ];
    } else {
      return [
        <Link className="nav-link"
            to={'/authentication/login'}>{t('Login')}</Link>,
        <Link className="nav-link"
            to={'/settings/'}>{t('Settings')}</Link>,
      ];
    }
  }

  renderHomeRoute = props => {
    const { authenticated } = this.state;
    return <Home {...props} authenticated={authenticated} />
  };

  renderAuthentication = props => {
    return <Authentication {...props} onAuthenticated={this.setAuthenticated} />
  }

  render() {
    const menuItems = this.getMenuItems();

    return (
      <div>
        <Navbar items={menuItems} authenticated={this.state.authenticated} account={this.state.account} />
        <div className='main-grid navbar-pushed'>
          <SideMenu items={menuItems} />
          <main role="main">
            <Route path='/' exact
                render={this.renderHomeRoute} />
            <Route path='/authentication' render={this.renderAuthentication} />
            <Route path='/settings/' exact component={Settings} />
            <Route path='/bird' component={Bird} />
            <Route path='/sighting' component={Sighting} />
          </main>
        </div>
      </div>
    );
  }
}

export default withTranslation()(Page);
