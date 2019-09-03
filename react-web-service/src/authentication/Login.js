import React, { Component } from 'react';
import { withTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js'
import { Link } from 'react-router-dom';
import LoginForm from './LoginForm.js';

class Login extends Component {

  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      loginErrorMessage: null,
    };
    this.authentication = new AuthenticationService();
  }

  setErrorMessage = message => {
    this.setState({ loginErrorMessage: message });
  }

  renderErrorMessage = () => {
    const { t } = this.props;
    const { loginErrorMessage } = this.state;
    if (loginErrorMessage) {
      return (
        <div className="row">
          <div className="col alert alert-danger" role="alert">
            {t(loginErrorMessage)}
          </div>
        </div>
      );
    }
    else {
      return null;
    }
  }

  render() {
    const { t } = this.props;
    return (
      <div className="container">
        <h1>{t('Login')}</h1>
        {this.renderErrorMessage()}
        <div className="d-flex justify-content-center">
          <div className="row">
            <div className="col">
              <div id="loginFormContainer">
                <LoginForm {...this.props} setErrorMessage={this.setErrorMessage} />
                <div className="row">
                  <Link to="/authentication/password-reset">
                    {t('Forgot your password?')}
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default withTranslation()(Login);
