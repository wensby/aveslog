import React, { Component } from 'react';
import { withTranslation } from 'react-i18next';
import Authentication from './authentication.js'

class Login extends Component {

  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      loginErrorMessage: null,
    };
    this.authentication = new Authentication();
  }

  handleLoginFormSubmit = async (event) => {
    try {
      event.preventDefault();
      const { username, password } = this.state;
      const response = await this.authentication.get_authentication_token(username, password);
      if (response.status === 'success') {
        localStorage.setItem('authToken', response.authToken);
        this.props.onAuthenticated();
        this.props.history.push("/");
      }
      else {
        this.setState({
          loginErrorMessage: 'Login failed.',
          username: '',
          password: '',
        });
      }
    } catch (e) {
      console.log(e);
    }
  }

  renderErrorMessage = () => {
    const { t } = this.props;
    const { loginErrorMessage } = this.state;
    if (loginErrorMessage) {
      return (
        <div className="row">
          <div className="col alert alert-danger" role="alert">
            { t(loginErrorMessage) }
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
                <form onSubmit={this.handleLoginFormSubmit}>
                  <div className="form-row">
                    <div className="form-group col-6">
                      <label htmlFor="usernameInput">{t('Username')}</label>
                      <input
                        value={this.state.username}
                        onChange={(event) => this.setState({username: event.target.value})}
                        id="usernameInput"
                        className="form-control"
                        type="text"
                        name="username"
                        placeholder={t('Username')}/>
                    </div>
                    <div className="form-group col-6">
                      <label htmlFor="passwordInput">{t('Password')}</label>
                      <input
                        value={this.state.password}
                        onChange={(event) => this.setState({password: event.target.value})}
                        id="passwordInput"
                        className="form-control"
                        type="password"
                        name="password"
                        placeholder={t('Password')}/>
                    </div>
                  </div>
                  <div className="d-flex flex-row">
                    <a className="btn btn-secondary" href="/">{t('Register new account')}</a>
                    <button type='submit' className="btn btn-primary ml-auto">{t('Login')}</button>
                  </div>
                </form>
                <div className="row">
                  <a href="/">{t('Forgot your password?')}</a>
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
