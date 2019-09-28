import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js';

export default () => {
  const [email, setEmail] = useState('');
  const [alert, setAlert] = useState(null);
  const { t } = useTranslation();
  const authentication = new AuthenticationService();

  const renderAlert = () => {
    if (alert) {
      return (
        <div className={`alert alert-${alert.type}`} role='alert'>
          { t(alert.message) }
        </div>
      );
    }
    return null;
  }

  const handleFormSubmit = async event => {
    try {
      event.preventDefault();
      const response = await authentication.postPasswordResetEmail(email);
      if (response.status === 'success') {
        setAlert({
          type: 'success',
          message: 'password-reset-email-submit-success-message'
        });
        setEmail('');
      }
      else {
        setAlert({
          type: 'danger',
          message: 'password-reset-email-submit-failure-message'
        });
        setEmail('');
      }
    } catch (e) {
      console.log(e);
    }
  }

  return (
    <div className='container'>
      <div className='row'>
        <div className='col'>
          <h1>{ t('Password Reset') }</h1>
          <p>{ t('password-reset-email-prompt-message') }</p>
          { renderAlert() }
          <form onSubmit={handleFormSubmit}>
            <div className='form-group'>
              <label htmlFor='emailInput'>{ t('Email') }</label>
              <input
                value={email}
                onChange={event => setEmail(event.target.value)}
                className='form-control'
                placeholder={ t('Email') }
                id='emailInput'
                name='email'
                type='text'/>
            </div>
            <button
              className='button'
              type='submit'>
              { t('Send') }
              </button>
          </form>
        </div>
      </div>
    </div>
  );
}
