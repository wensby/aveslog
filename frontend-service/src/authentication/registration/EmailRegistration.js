import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from '../AuthenticationService.js';
import { Link } from 'react-router-dom'
import { PageHeading } from '../../PageHeading';
import './EmailRegistration.scss';
import { Alert } from '../../generic/Alert.js';

export default () => {
  const [email, setEmail] = useState('');
  const [alert, setAlert] = useState(null);
  const { t } = useTranslation();
  const authentication = new AuthenticationService();

  const renderAlert = () => {
    if (alert) {
      return <Alert type={alert.type} message={t(alert.message)} />;
    }
    else {
      return null;
    }
  }

  const handleFormSubmit = async event => {
    try {
      event.preventDefault();
      const response = await authentication.postRegistrationEmail(email);
      if (response.status === 201) {
        setAlert({
          type: 'success',
          message: 'registration-email-submit-success-message',
        });
      }
      else {
        setAlert({
          type: 'danger',
          message: 'registration-email-submit-failure-message',
        });
        setEmail('');
      }
    }
    catch (e) {
      console.log(e);
    }
  }

  return (
    <div className='container'>
      <div className='row'>
        <div className='col'>
          <PageHeading>{t('Registration')}</PageHeading>
          <p>{t('register-link-request-prompt-message')}</p>
        </div>
      </div>
      {renderAlert()}
      <div className='row'>
        <div className='col'>
          <form onSubmit={handleFormSubmit} className='email-registration-form'>
            <div className='form-group'>
              <label htmlFor='emailInput'>{t('Email address')}</label>
              <input
                value={email}
                onChange={event => setEmail(event.target.value)}
                id='emailInput'
                className='form-control'
                type='text'
                name='email'
                placeholder={t('Enter email')}
              />
            </div>
            <button
              className='button'
              type='submit'>
              {t('Continue')}
            </button>
          </form>
        </div>
      </div>
      <div className='row mt-2'>
        <div className='col'>
          <Link to='/authentication/login'>{t('Back to login')}</Link>
        </div>
      </div>
    </div>
  );
}
