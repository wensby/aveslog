import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import NewPasswordFormGroup from '../NewPasswordFormGroup';
import { CredentialsRegistrationContext } from './CredentialsRegistration';
import './CredentialsRegistrationForm.scss'
import { FormGroup } from '../../generic/FormGroup';


export const CredentialsRegistrationForm = ({ }) => {
  const { email, takenUsernames, submit } = useContext(CredentialsRegistrationContext);
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
      submit([username, password]);
    }
    setShowFeedback(true);
  }

  return (
    <form className='credentials-form' onSubmit={handleSubmit} >
      <EmailFormGroup value={email} />
      <UsernameFormGroup value={username} onChange={setUsername}
        valid={usernameValid} showFeedback={showFeedback} />
      <NewPasswordFormGroup onChange={setPassword}
        showFeedback={showFeedback} />
      <SubmitButton />
    </form>
  );
};

const EmailFormGroup = ({ value }) => {
  const { t } = useTranslation();
  return (
    <FormGroup>
      <label htmlFor='emailInput'>{t('Email address')}</label>
      <input id='emailInput' readOnly name='email' value={value} />
    </FormGroup>
  );
};

const UsernameFormGroup = ({ value, onChange, valid, showFeedback }) => {
  const { t } = useTranslation();
  const validClassName = valid ? 'is-valid' : 'is-invalid';
  const className = showFeedback ? validClassName : null;

  return (
    <FormGroup>
      <label htmlFor='usernameInput'>{t('Username')}</label>
      <input id='usernameInput' className={className}
        type='text' aria-describedby='usernameHelpBlock'
        placeholder={t('Username')} value={value}
        onChange={event => onChange(event.target.value)} />
      <small id='usernameHelpBlock'>{t('username-help-block')}</small>
      <div className='valid-feedback'>{t('username-valid-feedback')}</div>
    </FormGroup>
  );
};

const SubmitButton = () => {
  const { t } = useTranslation();
  return <button type='submit'>{t('registration-button')}</button>;
};