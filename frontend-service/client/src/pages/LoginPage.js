import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { LoginForm } from '../authentication/LoginForm.js';
import { PageHeading } from '../generic/PageHeading.js';
import { Alert } from '../generic/Alert.js';
import './LoginPage.scss';

const Separator = () => {
  return <div className='separator' />;
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
  const [errorMessage, setErrorMessage] = useState(null);
  const { t } = useTranslation();

  return (
    <div className='login-page'>
      <PageHeading>{t('Login')}</PageHeading>
      {errorMessage && <ErrorMessage message={errorMessage} />}
      <LoginForm onError={setErrorMessage} />
      <div className='credentials-recovery-link'>
        <Link to='/authentication/credentials-recovery'>
          {t('credentials-recovery-link')}
        </Link>
      </div>
      <Separator />
      <NewAccountSection />
    </div>)
    ;
};

function ErrorMessage({ message }) {
  const { t } = useTranslation();

  return (
    <div className='row'>
      <Alert type='danger' message={t(message)} />
    </div>
  );
}
