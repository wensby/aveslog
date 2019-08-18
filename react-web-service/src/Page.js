import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Navbar from './navbar/navbar.js';
import SideMenu from './sidemenu.js';
import Login from './authentication/Login.js'
import Register from './authentication/Register.js'
import PasswordReset from './authentication/PasswordReset.js'
import Settings from './settings/settings'
import Home from './home/home.js';
import './App.css';
import { withTranslation } from 'react-i18next';
import AuthenticationService from './authentication/AuthenticationService.js';
import Authentication from './authentication/Authentication.js'
import AccountService from './account/AccountService';

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
            to={'/sighting/'}>{t('Sightings')}</Link>,
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

  renderLoginRoute = (props) => {
    return <Login {...props} onAuthenticated={this.setAuthenticated} />
  };

  renderHomeRoute = props => {
    const { authenticated } = this.state;
    return <Home {...props} authenticated={authenticated} />
  };

  renderPasswordResetRoute = props => {
    return <PasswordReset {...props} />
  }

  renderRegisterRoute = props => {
    return <Register {...props} />
  }

  renderAuthentication = props => {
    return <Authentication {...props} onAuthenticated={this.setAuthenticated} />
  }

  render() {
    const menuItems = this.getMenuItems();

    return (
      <Router>
        <Navbar items={menuItems} authenticated={this.state.authenticated} account={this.state.account} />
        <div className='main-grid navbar-pushed'>
          <SideMenu items={menuItems} />
          <main role="main" className="col-12 col-md-9 col-lg-8">
            <Route path='/' exact
                render={this.renderHomeRoute} />
            <Route path='/authentication' render={this.renderAuthentication} />
            <Route path='/settings/' exact component={Settings} />
          </main>
        </div>
      </Router>
    );
  }
}

export default withTranslation()(Page);
