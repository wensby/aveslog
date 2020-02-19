import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

export default ({ onChange, showFeedback }) => {
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');
  const [validPattern, setValidPattern] = useState(false);
  const [passwordsMatch, setPasswordsMatch] = useState(false);

  useEffect(() => {
    setValidPattern(/^.{8,128}$/.test(password));
    setPasswordsMatch(password === passwordConfirmation);
  }, [password, passwordConfirmation]);

  useEffect(() => {
    const validPassword = validPattern && passwordsMatch ? password : '';
    onChange(validPassword);
  }, [validPattern, passwordsMatch, onChange, password])

  return <>
    <PasswordFormGroup value={password} onChange={setPassword}
      valid={validPattern} showFeedback={showFeedback} />
    <PasswordConfirmationFormGroup value={passwordConfirmation}
      onChange={setPasswordConfirmation}
      valid={passwordsMatch} showFeedback={showFeedback} />
  </>;
}

const PasswordFormGroup = ({ value, onChange, valid, showFeedback }) => {
  const { t } = useTranslation();
  const validClassName = valid ? ' is-valid' : ' is-invalid';
  const feedbackClass = showFeedback ? validClassName : '';

  return (
    <div className='form-group'>
      <label htmlFor='passwordInput'>{t('Password')}</label>
      <input id='passwordInput' className={`form-input ${feedbackClass}`}
        type='password' name='password' aria-describedby='passwordHelpBlock'
        placeholder={t('Password')} value={value}
        onChange={event => onChange(event.target.value)} />
      <small id='passwordHelpBlock'>
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
        className={`form-input ${feedbackClass}`} value={value}
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
