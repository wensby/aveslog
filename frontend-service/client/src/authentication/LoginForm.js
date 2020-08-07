import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory } from "react-router-dom";
import { Spinner } from '../generic/Spinner.js';
import './LoginForm.scss';
import { AuthenticationContext } from './AuthenticationContext.js';

export function LoginForm({ onError }) {
  const history = useHistory();
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { t } = useTranslation();
  const { login } = useContext(AuthenticationContext);

  const handleLoginFormSubmit = event => {
    event.preventDefault();
    setLoading(true);
    login(username, password)
      .then(__ => history.push('/home'))
      .catch(__ => {
        setLoading(false);
        onError('Login failed.');
        setUsername('');
        setPassword('');
      });
  }

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
          {loading && <div style={{ marginRight: '10px', width: '20px', height: '20px' }}><Spinner /></div>}
          <button type='submit'>{t('Login')}</button>
        </div>
      </div>
    </form>
  );
}
