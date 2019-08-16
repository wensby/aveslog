import React, { Component } from 'react';
import { withTranslation } from 'react-i18next';
import Authentication from './authentication';
import { Link } from 'react-router-dom'

class PasswordReset extends Component {

  constructor(props) {
    super(props);
    this.state = {
      email: '',
      alert: null,
    }
    this.authentication = new Authentication();
  }

  renderAlert = () => {
    const { t } = this.props;
    const { alert } = this.state;
    if (alert) {
      return (
        <div className={ `col alert alert-${alert.type}` }
          role="alert">{ t(alert.message) }</div>
      );
    }
    else {
      return null;
    }
  }

  handleFormSubmit = async event => {
    try {
      event.preventDefault();
      const { email } = this.state;
      const response = await this.authentication.post_registration_email(email);
      if (response.status === 'success') {
        this.setState({
          alert: {
            type: 'success',
            message: 'registration-email-submit-success-message',
          }
        });
      }
      else {
        this.setState({
          alert: {
            type: 'danger',
            message: 'registration-email-submit-failure-message',
          },
          email: '',
        });
      }
    }
    catch (e) {
      console.log(e);
    }
  }

  onEmailInputChanged = event => {
    this.setState({
      email: event.target.value
    });
  }

  render() {
    const { t } = this.props;
    const { email } = this.state;
    return (
      <div className="container">
        <div className="row">
          <div className="col">
            <h1>{ t('Registration') }</h1>
            <p>{ t('register-link-request-prompt-message') }</p>
          </div>
        </div>
        {this.renderAlert()}
        <div className="row">
          <div className="col">
            <form onSubmit={this.handleFormSubmit}>
              <div className="form-group">
                <label htmlFor="emailInput">{ t('Email address') }</label>
                <input
                  value={email}
                  onChange={this.onEmailInputChanged}
                  id="emailInput"
                  className="form-control"
                  type="text"
                  name="email"
                  placeholder={ t('Enter email') }
                  />
              </div>
              <button
                className="btn btn-primary"
                type="submit">
                { t('Continue') }
                </button>
            </form>
          </div>
        </div>
        <div className="row mt-2">
          <div className="col">
            <Link to='/authentication/login'>{ t('Back to login') }</Link>
          </div>
        </div>
      </div>
    );
  }
}

export default withTranslation()(PasswordReset);
