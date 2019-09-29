import React, { useState } from 'react';
import { useTranslation } from "react-i18next";
import NewPasswordFormGroup from '../authentication/NewPasswordFormGroup';

const PasswordChangeForm = () => {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);
  const { t } = useTranslation();

  const handleFormSubmit = async event => {
    event.preventDefault();
    if (newPassword) {
      // make request
    }
    setShowFeedback(true);
  };

  return <form onSubmit={handleFormSubmit}>
    <div>
      <label htmlFor='currentPassword'>{t('current-password')}</label>
      <input className='form-input' id='currentPassword' type='text'
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
