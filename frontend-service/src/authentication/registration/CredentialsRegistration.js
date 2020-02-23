import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from '../AuthenticationService.js';
import { CredentialsForm } from './CredentialsForm';
import { UserContext } from '../UserContext.js';
import { useHistory } from "react-router-dom";
import { PageHeading } from '../../generic/PageHeading.js';
import { Alert } from '../../generic/Alert';
import './CredentialsRegistration.scss';

export const CredentialsRegistration = ({ token, registrationRequest, onSuccess }) => {
  const { setRefreshToken } = useContext(UserContext);
  const [takenUsernames, setTakenUsernames] = useState([]);
  const [alert, setAlert] = useState(null);
  const { t } = useTranslation();
  const history = useHistory();
  const email = registrationRequest ? registrationRequest.email : '';

  const handleFormSubmit = async credentials => {
    try {
      const response = await new AuthenticationService().postRegistration(token, credentials);
      if (response.status === 201) {
        onSuccess();
        const response = await new AuthenticationService().postRefreshToken(credentials[0], credentials[1]);
        if (response.status === 201) {
          const refreshResponseJson = await response.json();
          setRefreshToken({
            id: refreshResponseJson.id,
            jwt: refreshResponseJson.refreshToken,
            expiration: Date.parse(refreshResponseJson.expirationDate),
          });
          history.push('/');
        }
      }
      else if (response.status === 409) {
        const json = await response.json();
        if (json['code'] === 3) {
          setTakenUsernames(takenUsernames.concat([credentials[0]]))
          setAlert({
            category: 'danger',
            message: 'Username already taken.',
          });
        }
      }
    }
    catch (err) {
    }
  };

  return (
    <div className='credentials-registration'>
      <PageHeading>{t('Registration')}</PageHeading>
      <p>{t('registration-form-instructions')}</p>
      {alert && <Alert type={alert.category} message={alert.message} />}
      <CredentialsForm email={email} onSubmit={handleFormSubmit} takenUsernames={takenUsernames} />
    </div>
  );
};
