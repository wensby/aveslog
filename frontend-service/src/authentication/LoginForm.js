import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js';
import { UserContext } from './UserContext.js';
import { useHistory } from "react-router-dom";
import './spinner.scss';
import './LoginForm.scss';

export function LoginForm({ onError }) {
  const history = useHistory();
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const authentication = new AuthenticationService();
  const { t } = useTranslation();
  const { setRefreshToken } = useContext(UserContext);

  const postRefreshToken = async () => {
    return authentication.postRefreshToken(username, password);
  }

  const handleLoginFormSubmit = async event => {
    try {
      event.preventDefault();
      setLoading(true);
      const response = await postRefreshToken();
      if (response.status === 201) {
        const refreshResponseJson = await response.json();
        setRefreshToken({
          id: refreshResponseJson.id,
          jwt: refreshResponseJson.refreshToken,
          expiration: Date.parse(refreshResponseJson.expirationDate),
        });
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
    finally {
      setLoading(false);
    }
  };

  return (
    <form className='login-form' onSubmit={handleLoginFormSubmit}>
      <div className='credentials-fields'>
        <div>
          <label htmlFor='usernameInput'>{t('username-label')}</label>
          <input value={username}
            onChange={event => setUsername(event.target.value)}
            id='usernameInput' className='form-control' type='text'
            name='username' placeholder={t('username-label')} />
        </div>
        <div>
        <label htmlFor='passwordInput'>{t('Password')}</label>
        <input value={password}
          onChange={event => setPassword(event.target.value)}
          id='passwordInput' className='form-control' type='password'
          name='password' placeholder={t('Password')} />
        </div>
      </div>
      <div className='login-button-row'>
        <div>
          {loading && <div className='spinner' />}
          <button type='submit' className='button'>
            {t('Login')}
          </button>
        </div>
      </div>
    </form>
  );
}
