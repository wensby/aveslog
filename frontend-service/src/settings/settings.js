import React, { useState, useContext } from 'react';
import { useTranslation } from "react-i18next";
import NewPasswordFormGroup from '../authentication/NewPasswordFormGroup';
import AuthenticationService from '../authentication/AuthenticationService';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { useReactRouter } from '../reactRouterHook.js';

const PasswordChangeForm = () => {
  const { history } = useReactRouter();
  const { token } = useContext(AuthenticationContext);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const { t } = useTranslation();
  const service = new AuthenticationService();

  const renderAlert = () => {
    if (errorMessage) {
      return (
        <div className='row'>
          <div className={`col alert alert-${errorMessage.category}`}
            role='alert'>{ errorMessage.message }</div>
        </div>
      );
    }
  }

  const handleFormSubmit = async event => {
    event.preventDefault();
    if (newPassword) {
      const response = await service.postPasswordUpdate(token, currentPassword, newPassword);
      if (response.status == 204) {
        history.push('/');
      }
      else {
        const message = (await response.json())['message'];
        setErrorMessage({category: 'danger', message: message});
      }
    }
    setShowFeedback(true);
  };

  return <form onSubmit={handleFormSubmit}>
    <div>
      {renderAlert()}
      <label htmlFor='currentPassword'>{t('current-password')}</label>
      <input className='form-input' id='currentPassword' type='password'
        placeholder={t('current-password')}
        value={currentPassword}
        onChange={event => setCurrentPassword(event.target.value)} />
    </div>
    <NewPasswordFormGroup onChange={setNewPassword}
        showFeedback={showFeedback} />
    <div>
      <button className='button'>{t('password-change-button')}</button>
    </div>
  </form>;
}

export default function Settings() {
  const { t } = useTranslation();

  return (
    <>
      <h1>{t('Settings')}</h1>
      <h2>{t('change-password')}</h2>
      <PasswordChangeForm />
    </>
  );
}
