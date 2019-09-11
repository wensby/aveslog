import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

export default ({ email, token, onSubmit }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { t } = useTranslation();

  return (<form onSubmit={onSubmit}>
    <div className='form-group'>
      <label htmlFor='emailInput'>{t('Email address')}</label>
      <input
        className='form-control'
        id='emailInput'
        type='text'
        name='email'
        readonly
        placeholder={email}
        value={email} />
    </div>
    <div className='form-group'>
      <label htmlFor='usernameInput'>{t('Username')}</label>
      <input
        id='usernameInput'
        className='form-control'
        type='username'
        name='username'
        aria-describedby='usernameHelpBlock'
        placeholder={t('Username')}
        required value={username}
        onChange={event => setUsername(event.target.value)}
        pattern='[A-Za-z0-9._-]{5,32}' />
      <small id='usernameHelpBlock' className='form-text text-muted'>
        {t('username-help-block')}
      </small>
      <div className='valid-feedback'>
        {t('Nice username!')}
      </div>
    </div>
    <div className='form-group'>
      <label htmlFor='passwordInput'>{t('Password')}</label>
      <input id='passwordInput'
        className='form-control'
        type='password'
        name='password'
        aria-describedby='passwordHelpBlock'
        placeholder={t('Password')}
        required value={password}
        onChange={event => setPassword(event.target.value)}
        pattern='.{8,128}' />
      <small id='passwordHelpBlock' className='form-text text-muted'>
        {t('password-format-help-message')}
      </small>
      <div className='valid-feedback'>
        {t('Seems long enough!')}
      </div>
      <div className='invalid-feedback'>
        {t('Needs more love.')}
      </div>
    </div>
    <div className='form-group'>
      <label htmlFor='confirmPasswordInput'>
        {t('password-confirm-password-label')}
      </label>
      <input
        id='confirmPasswordInput'
        className='form-control'
        type='password'
        name='confirmPassword'
        placeholder={t('password-confirm-password-label')} />
      <div className='valid-feedback'>
        {t('Both passwords matches!')}
      </div>
      <div className='invalid-feedback'>
        {t("Doesn't match your password above.")}
      </div>
    </div>
    <div className='form-group'>
      <div className='form-check'>
        <input className='form-check-input'
          type='checkbox'
          value=''
          id='tocCheckbox'
          required />
        <label className='form-check-label' htmlFor='tocCheckbox'>
          {t('terms-and-conditions-checkbox-label')}
        </label>
        <div className='invalid-feedback'>
          {t('You must agree before submitting.')}
        </div>
      </div>
    </div>
    <input type='hidden' name='token' value={token} />
    <button class='btn btn-primary' type='submit'>
      {t('registration-button')}
    </button>
  </form>);
}
