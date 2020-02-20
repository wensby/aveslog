import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js';
import { Alert } from '../generic/Alert.js';
import './CreatePasswordReset.scss';

export default () => {
  const [email, setEmail] = useState('');
  const [alert, setAlert] = useState(null);
  const { t } = useTranslation();
  const authentication = new AuthenticationService();

  const renderAlert = () => {
    if (alert) {
      return (
        <Alert type={alert.type} message={t(alert.message)} />
      );
    }
    return null;
  }

  const handleFormSubmit = async event => {
    try {
      event.preventDefault();
      const response = await authentication.postPasswordResetEmail(email);
      if (response.status === 200) {
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
    <div class='create-password-reset'>
      <div>
        <div>
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
            <button type='submit'>{ t('Send') }</button>
          </form>
        </div>
      </div>
    </div>
  );
}
