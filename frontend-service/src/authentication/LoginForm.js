import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js';
import { Link } from 'react-router-dom';
import { AuthenticationContext } from './AuthenticationContext.js';
import { useReactRouter } from '../reactRouterHook.js';

export default ({ onError }) => {
  const { history } = useReactRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const authentication = new AuthenticationService();
  const { t } = useTranslation();
  const { onAuthenticated } = useContext(AuthenticationContext);

  const handleLoginFormSubmit = async (event) => {
    try {
      event.preventDefault();
      const response = await authentication.fetchAuthenticationToken(username, password);
      if (response.status === 'success') {
        onAuthenticated(response.authToken);
        history.push('/');
      }
      else {
        onError('Login failed.');
        setUsername('');
        setPassword('');
      }
    }
    catch (e) {
      console.log(e);
    }
  };

  return (
    <form className='login-form' onSubmit={handleLoginFormSubmit}>
      <div className='form-row'>
        <div className='form-group col-6'>
          <label htmlFor='usernameInput'>{t('username-label')}</label>
          <input value={username}
            onChange={event => setUsername(event.target.value)}
            id='usernameInput' className='form-control' type='text'
            name='username' placeholder={t('username-label')} />
        </div>
        <div className='form-group col-6'>
          <label htmlFor='passwordInput'>{t('Password')}</label>
          <input value={password}
            onChange={event => setPassword(event.target.value)}
            id='passwordInput' className='form-control' type='password'
            name='password' placeholder={t('Password')} />
        </div>
      </div>
      <div className='d-flex flex-row'>
        <button type='submit' className='btn ml-auto login-button'>
          {t('Login')}
        </button>
      </div>
    </form>
  );
}
