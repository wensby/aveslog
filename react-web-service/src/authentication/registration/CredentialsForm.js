import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';


export default ({ email, token, onSubmit }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');
  const [usernameValid, setUsernameValid] = useState(false);
  const [passwordValid, setPasswordValid] = useState(false);
  const [passwordsMatch, setPasswordsMatch] = useState(false);
  const [showFeedback, setShowFeedback] = useState(false);

  useEffect(() => {
    setUsernameValid(/^[A-Za-z0-9._-]{5,32}$/.test(username));
    setPasswordValid(/^.{8,128}$/.test(password));
    setPasswordsMatch(password == passwordConfirmation);
  }, [username, password, passwordConfirmation]);

  const handleSubmit = event => {
    event.preventDefault();
    if (usernameValid && passwordValid && passwordsMatch) {
      onSubmit([username, password]);
    }
    else {
      setShowFeedback(true);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <EmailFormGroup value={email} />
      <UsernameFormGroup value={username} onChange={setUsername}
        valid={usernameValid} showFeedback={showFeedback} />
      <PasswordFormGroup value={password} onChange={setPassword}
        valid={passwordValid} showFeedback={showFeedback} />
      <PasswordConfirmationFormGroup value={passwordConfirmation}
        onChange={setPasswordConfirmation}
        valid={passwordsMatch} showFeedback={showFeedback} />
      <input type='hidden' name='token' value={token} />
      <SubmitButton />
    </form>
  );
}

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

const PasswordFormGroup = ({ value, onChange, valid, showFeedback }) => {
  const { t } = useTranslation();
  const validClassName = valid ? ' is-valid' : ' is-invalid';
  const feedbackClass = showFeedback ? validClassName : '';

  return (
    <div className='form-group'>
      <label htmlFor='passwordInput'>{t('Password')}</label>
      <input id='passwordInput' className={`form-control ${feedbackClass}`}
        type='password' name='password' aria-describedby='passwordHelpBlock'
        placeholder={t('Password')} value={value}
        onChange={event => onChange(event.target.value)} />
      <small id='passwordHelpBlock' className='form-text text-muted'>
        {t('password-format-help-message')}
      </small>
      <div className='valid-feedback'>{t('password-valid-feedback')}</div>
      <div className='invalid-feedback'>{t('password-invalid-feedback')}</div>
    </div>
  );
};

const PasswordConfirmationFormGroup = props => {
  const { value, onChange, valid, showFeedback } = props;
  const { t } = useTranslation();
  const validClassName = valid && value ? ' is-valid' : ' is-invalid';
  const feedbackClass = showFeedback ? validClassName : '';

  return (
    <div className='form-group'>
      <label htmlFor='confirmPasswordInput'>
        {t('password-confirm-password-label')}
      </label>
      <input id='confirmPasswordInput' type='password' name='confirmPassword'
        className={`form-control ${feedbackClass}`} value={value}
        placeholder={t('password-confirm-password-label')}
        onChange={event => onChange(event.target.value)} />
      <div className='valid-feedback'>
        {t('password-confirmation-valid-feedback')}
      </div>
      <div className='invalid-feedback'>
        {t('password-confirmation-invalid-feedback')}
      </div>
    </div>
  );
};

const SubmitButton = () => {
  const { t } = useTranslation();
  return (
    <button className='btn btn-primary' type='submit'>
      {t('registration-button')}
    </button>
  );
};
