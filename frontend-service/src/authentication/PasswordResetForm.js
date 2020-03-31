import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from './AuthenticationService.js';
import NewPasswordFormGroup from './NewPasswordFormGroup';
import { Alert } from '../generic/Alert.js';

export const PasswordResetForm = props => {
  const { t } = useTranslation();
  const token = props.match.params.token;
  const [alert, setAlert] = useState(null);
  const [password, setPassword] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);

  const renderAlert = () => {
    if (alert) {
      return <Alert type={alert.type} message={t(alert.message)}/>;
    }
    else {
      return null;
    }
  };

  const submitForm = async event => {
    event.preventDefault();
    if (password) {
      try {
        const service = new AuthenticationService();
        const response = await service.postPasswordResetPassword(token, password);
        if (response.status === 200) {
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
    }
    else {
      setShowFeedback(true);
    }
  };

  return (
    <div>
      <div>
        <div>
          <h1>{ t('password-reset-title') }</h1>
          <p>{ t('password-reset-form-prompt-message') }</p>
          {renderAlert()}
          <form onSubmit={submitForm}>
            <NewPasswordFormGroup onChange={setPassword}
              showFeedback={showFeedback} />
            <button type='submit'>{ t('button-submit-label') }</button>
          </form>
        </div>
      </div>
    </div>
  );
};
