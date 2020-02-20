import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from '../AuthenticationService.js';
import { Link } from 'react-router-dom'
import { PageHeading } from '../../generic/PageHeading.js';
import { Alert } from '../../generic/Alert.js';
import './EmailRegistrationPage.scss';

const PageContext = React.createContext();

export const EmailRegistrationPage = () => {
  const [email, setEmail] = useState('');
  const [alert, setAlert] = useState(null);
  const { t } = useTranslation();
  const authentication = new AuthenticationService();

  const submit = async () => {
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
    }
    setEmail('');
  }

  return (
    <PageContext.Provider value={{ email, setEmail, submit, alert }}>
      <div className='email-registration-page'>
        <PageHeading>{t('Registration')}</PageHeading>
        <p>{t('register-link-request-prompt-message')}</p>
        {alert && <SubmitAlert alert={alert} />}
        <Form />
        <Link to='/authentication/login'>{t('Back to login')}</Link>
      </div>
    </PageContext.Provider>
  );
};

const SubmitAlert = ({ alert }) => {
  const { t } = useTranslation();
  return <Alert type={alert.type} message={t(alert.message)} />
}

const Form = () => {
  const { email, setEmail, submit } = useContext(PageContext);
  const { t } = useTranslation();

  const handleSubmit = event => {
    event.preventDefault();
    submit();
  };

  const handleEmailChange = event => {
    setEmail(event.target.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor='email'>{t('Email address')}</label>
        <input value={email} onChange={handleEmailChange} id='email' className='form-control'
          type='text' placeholder={t('Enter email')} />
      </div>
      <button type='submit'>{t('Continue')}</button>
    </form>
  );
};
