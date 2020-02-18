import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import NewPasswordFormGroup from '../NewPasswordFormGroup';


export const CredentialsForm = ({ email, token, onSubmit, takenUsernames }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [usernameValid, setUsernameValid] = useState(false);
  const [showFeedback, setShowFeedback] = useState(false);

  useEffect(() => {
    setUsernameValid(!takenUsernames.includes(username) && /^[A-Za-z0-9._-]{5,32}$/.test(username));
  }, [takenUsernames, username]);

  const handleSubmit = event => {
    event.preventDefault();
    if (usernameValid && password) {
      onSubmit([username, password]);
    }
    setShowFeedback(true);
  }

  return (
    <form onSubmit={handleSubmit}>
      <EmailFormGroup value={email} />
      <UsernameFormGroup value={username} onChange={setUsername}
        valid={usernameValid} showFeedback={showFeedback} />
      <NewPasswordFormGroup onChange={setPassword}
        showFeedback={showFeedback} />
      <input type='hidden' name='token' value={token} />
      <SubmitButton />
    </form>
  );
};

const EmailFormGroup = ({ value }) => {
  const { t } = useTranslation();
  return (
    <div className='form-group'>
      <label htmlFor='emailInput'>{t('Email address')}</label>
      <input id='emailInput' readOnly className='form-control' type='email'
        name='email' value={value} />
    </div>
  );
};

const UsernameFormGroup = ({ value, onChange, valid, showFeedback }) => {
  const { t } = useTranslation();
  const validClassName = valid ? ' is-valid' : ' is-invalid';
  const feedbackClass = showFeedback ? validClassName : '';

  return (
    <div className='form-group'>
      <label htmlFor='usernameInput'>{t('Username')}</label>
      <input id='usernameInput' className={`form-control${feedbackClass}`}
        type='text' name='username' aria-describedby='usernameHelpBlock'
        placeholder={t('Username')} value={value}
        onChange={event => onChange(event.target.value)} />
      <small id='usernameHelpBlock' className='form-text text-muted'>
        {t('username-help-block')}
      </small>
      <div className='valid-feedback'>{t('username-valid-feedback')}</div>
    </div>
  );
};

const SubmitButton = () => {
  const { t } = useTranslation();
  return (
    <button className='button' type='submit'>
      {t('registration-button')}
    </button>
  );
};
