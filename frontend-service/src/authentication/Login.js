import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import LoginForm from './LoginForm.js';
import './login.css';

const Separator = () => {
  return <div className='separator'/>;
}

const NewAccountSection = () => {
  const { t } = useTranslation();
  return <div className='new-account-section'>
    <p className='bold-question'>{t('new-user-question')}</p>
    <Link to='/authentication/registration'>
      {t('Register new account')}
    </Link>
  </div>
}

export default () => {
  const [loginErrorMessage, setLoginErrorMessage] = useState(null);
  const { t } = useTranslation();

  const setErrorMessage = message => {
    setLoginErrorMessage(message);
  }

  const renderErrorMessage = () => {
    if (loginErrorMessage) {
      return (
        <div className='row'>
          <div className='col alert alert-danger' role='alert'>
            {t(loginErrorMessage)}
          </div>
        </div>
      );
    }
    else {
      return null;
    }
  }

  return <div className='login'>
    <h1>{t('Login')}</h1>
    {renderErrorMessage()}
    <LoginForm onError={setErrorMessage} />
    <div className='password-recover-link'>
      <Link  to='/authentication/password-reset'>
        {t('password-recover-link')}
      </Link>
    </div>
    <Separator />
    <NewAccountSection />
  </div>;
}
