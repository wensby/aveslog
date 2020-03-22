import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js';
import { useHistory } from "react-router-dom";
import { Spinner } from '../generic/Spinner.js';
import './LoginForm.scss';
import { AuthenticationContext } from './AuthenticationContext.js';

export function LoginForm({ onError }) {
  const history = useHistory();
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const authentication = new AuthenticationService();
  const { t } = useTranslation();
  const { setRefreshToken } = useContext(AuthenticationContext);

  const postRefreshToken = async () => {
    return authentication.postRefreshToken(username, password);
  }

  const handleLoginFormSubmit = async event => {
    try {
      event.preventDefault();
      setLoading(true);
      const response = await postRefreshToken();
      setLoading(false);
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
          {true && <div style={{marginRight: '10px', width: '20px', height: '20px'}}><Spinner /></div>}
          <button type='submit'>{t('Login')}</button>
        </div>
      </div>
    </form>
  );
}
