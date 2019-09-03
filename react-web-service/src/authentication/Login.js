import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import LoginForm from './LoginForm.js';

export default () => {
  const [loginErrorMessage, setLoginErrorMessage] = useState(null);
  const { t } = useTranslation();

  const setErrorMessage = message => {
    setLoginErrorMessage(message);
  }

  const renderErrorMessage = () => {
    if (loginErrorMessage) {
      return (
        <div className="row">
          <div className="col alert alert-danger" role="alert">
            {t(loginErrorMessage)}
          </div>
        </div>
      );
    }
    else {
      return null;
    }
  }

  return (
    <div className='container'>
      <h1>{t('Login')}</h1>
      {renderErrorMessage()}
      <div className='d-flex justify-content-center'>
        <div className='row'>
          <div className='col'>
            <div id='loginFormContainer'>
              <LoginForm setErrorMessage={setErrorMessage} />
              <div className='row'>
                <Link to='/authentication/password-reset'>
                  {t('Forgot your password?')}
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
