import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js';

export default function PasswordResetForm(props) {
  const { t } = useTranslation();
  const token = props.match.params.token;
  const [alert, setAlert] = useState(null);
  const [password, setPassword] = useState('');

  const renderAlert = () => {
    if (alert) {
      return (
        <div className={`alert alert-${alert.type}`} role='alert'>
          { t(alert.message) }
        </div>
      );
    }
    else {
      return null;
    }
  };

  const submitForm = async event => {
    try {
      event.preventDefault();
      const service = new AuthenticationService();
      const response = await service.postPasswordResetPassword(token, password);
      if (response.status === 'success') {
        setAlert({
          type: 'success',
          message: 'password-reset-success-alert-message',
        });
      }
      else {
        setAlert({
          type: 'danger',
          message: 'password-reset-failure-alert-message',
        });
      }
      setPassword('');
    }
    catch (err) {
      
    }
  };

  return (
    <div className='container'>
      <div className='row'>
        <div className='col'>
          <h1>{ t('password-reset-title') }</h1>
          <p>{ t('password-reset-form-prompt-message') }</p>
          {renderAlert()}
          <form onSubmit={submitForm}>
            <div className='form-group'>
              <label htmlFor='passwordInput'>{ t('Password') }</label>
              <input id='passwordInput'
                className='form-control'
                value={password}
                onChange={event => setPassword(event.target.value)}
                type='password'
                name='password'
                aria-describedby='passwordHelpBlock'
                placeholder={ t('Password') }
                required pattern='.{8,128}'/>
              <small id='passwordHelpBlock'
                className='form-text text-muted'>
                { t('password-format-help-message') }</small>
            </div>
            <div className='form-group'>
              <label htmlFor='confirmPasswordInput'>
                { t('password-confirm-password-label') }</label>
              <input id='confirmPasswordInput'
                className='form-control'
                type='password'
                name='confirmPassword'
                placeholder={ t('password-confirm-password-label') }/>
            </div>
            <button className='button'
              type='submit'>{ t('button-submit-label') }</button>
          </form>
        </div>
      </div>
    </div>
  );
}
