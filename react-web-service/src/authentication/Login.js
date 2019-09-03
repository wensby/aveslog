import React, { Component, useState, useContext } from 'react';
import { withTranslation, useTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js'
import { Link } from 'react-router-dom';
import { AuthenticationContext } from './AuthenticationContext.js';

function LoginForm(props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const authentication = new AuthenticationService();
  const { t } = useTranslation();
  const { onAuthenticated } = useContext(AuthenticationContext);

  const handleLoginFormSubmit = async event => {
    try {
      event.preventDefault();
      const response = await authentication.fetchAuthenticationToken(username, password);
      if (response.status === 'success') {
        onAuthenticated(response.authToken);
        props.history.push("/");
      }
      else {
        props.setErrorMessage('Login failed.');
        setUsername('');
        setPassword('');
      }
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <form onSubmit={handleLoginFormSubmit}>
      <div className="form-row">
        <div className="form-group col-6">
          <label htmlFor="usernameInput">{t('Username')}</label>
          <input
            value={username}
            onChange={event => setUsername(event.target.value)}
            id="usernameInput"
            className="form-control"
            type="text"
            name="username"
            placeholder={t('Username')} />
        </div>
        <div className="form-group col-6">
          <label htmlFor="passwordInput">{t('Password')}</label>
          <input
            value={password}
            onChange={event => setPassword(event.target.value)}
            id="passwordInput"
            className="form-control"
            type="password"
            name="password"
            placeholder={t('Password')} />
        </div>
      </div>
      <div className="d-flex flex-row">
        <Link
          to="/authentication/register"
          className="btn btn-secondary">
          {t('Register new account')}</Link>
        <button type='submit' className="btn btn-primary ml-auto">{t('Login')}</button>
      </div>
    </form>
  );
}

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
