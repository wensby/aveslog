import React, { Component } from 'react';
import { withTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js';

class CreatePasswordReset extends Component {

  constructor(props) {
    super(props);
    this.state = {
      email: '',
      alert: null,
    }
    this.authentication = new AuthenticationService();
  }

  renderAlert = () => {
    const { t } = this.props;
    const { alert } = this.state;

    if (alert) {
      return (
        <div className={`alert alert-${alert.type}`} role="alert">
          { t(alert.message) }
        </div>
      );
    }
    return null;
  }

  handleFormSubmit = async event => {
    try {
      event.preventDefault();
      const { email } = this.state;
      const response = await this.authentication.postPasswordResetEmail(email);
      if (response.status === 'success') {
        this.setState({
          alert: {
            type: 'success',
            message: 'password-reset-email-submit-success-message'
          },
          email: '',
        });
      }
      else {
        this.setState({
          alert: {
            type: 'danger',
            message: 'password-reset-email-submit-failure-message',
          },
          email: '',
        });
      }
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    const { t } = this.props;
    return (
      <div className="container">
        <div className="row">
          <div className="col">
            <h1>{ t('Password Reset') }</h1>
            <p>{ t('password-reset-email-prompt-message') }</p>
            { this.renderAlert() }
            <form onSubmit={this.handleFormSubmit}>
              <div className="form-group">
                <label htmlFor="emailInput">{ t('Email') }</label>
                <input
                  value={this.state.email}
                  onChange={event => this.setState({email: event.target.value})}
                  className='form-control'
                  placeholder={ t('Email') }
                  id="emailInput"
                  name="email"
                  type="text"/>
              </div>
              <button
                className="btn btn-primary"
                type="submit">
                { t('Send') }
                </button>
            </form>
          </div>
        </div>
      </div>
    );
  }
}

export default withTranslation()(CreatePasswordReset);
