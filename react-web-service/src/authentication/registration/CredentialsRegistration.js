import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useReactRouter } from '../../reactRouterHook';
import AuthenticationService from '../AuthenticationService.js';
import RegistrationForm from './CredentialsForm';

export default () => {
  const { match } = useReactRouter();
  const token = match.params.token;
  const [alert, setAlert] = useState(null);
  const [email, setEmail] = useState('');

  const { t } = useTranslation();
  const authentication = new AuthenticationService();

  const fetchEmail = async () => {
    const registration = await authentication.fetchRegistration(token);
    if (registration) {
      setEmail(registration['email']);
    }
  }

  useEffect(() => {
    fetchEmail();
  }, []);

  const renderAlert = () => {
    if (alert) {
      return (
        <div className='row'>
          <div className={`col alert alert-${alert.category}`} role='alert'>
            { alert.message }
          </div>
        </div>
      );
    }
  }

  const handleFormSubmit = async event => {
    try {
      event.preventDefault();
    }
    catch (err) {
    }
  };

  return (
    <div className='container'>
      <div className='row'>
        <div className='col'>
          <h2>{ t('Registration') }</h2>
          <p>
            { t('registration-form-instructions') }
          </p>
        </div>
      </div>
      {renderAlert()}
      <div className='row'>
        <div className='col'>
          <RegistrationForm
            email={email}
            token={token}
            onSubmit={handleFormSubmit} />
        </div>
      </div>
    </div>
  );
}
