import React, { Component } from 'react';
import { withTranslation } from 'react-i18next';
import Authentication from './authentication.js'

class Login extends Component {

  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
    };
  }

  login = async (event) => {
    try {
      event.preventDefault();
      const { username, password } = this.state;
      await (new Authentication().login(username, password));
      this.props.onAuthenticated();
      this.props.history.push("/");
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    const { t } = this.props;
    return (
      <div className="container">
        <h1>{t('Login')}</h1>
        <div className="d-flex justify-content-center">
          <div className="row">
            <div className="col">
              <div id="loginFormContainer">
                <form onSubmit={this.login}>
                  <div className="form-row">
                    <div className="form-group col-6">
                      <label htmlFor="usernameInput">{t('Username')}</label>
                      <input onChange={(event) => this.setState({username: event.target.value})} id="usernameInput" className="form-control" type="text" name="username" placeholder={t('Username')}/>
                    </div>
                    <div className="form-group col-6">
                      <label htmlFor="passwordInput">{t('Password')}</label>
                      <input onChange={(event) => this.setState({password: event.target.value})} id="passwordInput" className="form-control" type="password" name="password" placeholder={t('Password')}/>
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