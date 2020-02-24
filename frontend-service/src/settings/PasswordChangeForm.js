import React, { useState, useContext } from 'react';
import { useTranslation } from "react-i18next";
import NewPasswordFormGroup from '../authentication/NewPasswordFormGroup';
import AuthenticationService from '../authentication/AuthenticationService';
import { UserContext } from '../authentication/UserContext';
import { useHistory } from "react-router-dom";
import { Alert } from '../generic/Alert';
import './PasswordChangeForm.scss';

export const PasswordChangeForm = () => {
  const history = useHistory();
  const { accessToken } = useContext(UserContext);
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
          <Alert type={errorMessage.category} message={errorMessage.message} />
        </div>
      );
    }
  }

  const handleFormSubmit = async event => {
    event.preventDefault();
    if (newPassword) {
      const response = await service.postPasswordUpdate(accessToken.jwt, currentPassword, newPassword);
      if (response.status === 204) {
        history.push('/');
      }
      else {
        const message = (await response.json())['message'];
        setErrorMessage({ category: 'danger', message: message });
      }
    }
    setShowFeedback(true);
  };

  return (
    <form onSubmit={handleFormSubmit} className='password-change-form'>
      {renderAlert()}
      <div className='form-group'>
        <label htmlFor='currentPassword'>{t('current-password')}</label>
        <input id='currentPassword' type='password'
          placeholder={t('current-password')}
          value={currentPassword}
          onChange={event => setCurrentPassword(event.target.value)} />
      </div>
      <NewPasswordFormGroup onChange={setNewPassword}
        showFeedback={showFeedback} />
      <button>{t('password-change-button')}</button>
    </form>
  );
}
