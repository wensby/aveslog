import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

export default function PasswordResetForm(props) {
  const { t } = useTranslation();
  const [alert, setAlert] = useState(null);

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
      setAlert({
        type: 'success',
        message: 'password-reset-success-alert-message',
      });
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
                { t('new-password-confirm-password-label') }</label>
              <input id='confirmPasswordInput'
                className='form-control'
                type='password'
                name='confirmPassword'
                placeholder={ t('new-password-confirm-password-label') }/>
            </div>
            <button className='btn btn-primary'
              type='submit'>{ t('button-submit-label') }</button>
          </form>
        </div>
      </div>
    </div>
  );
}
