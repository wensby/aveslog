import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import AuthenticationService from '../AuthenticationService.js';
import { CredentialsRegistrationForm } from './CredentialsRegistrationForm';
import { useHistory } from "react-router-dom";
import { PageHeading } from '../../generic/PageHeading.js';
import { Alert } from '../../generic/Alert';
import './CredentialsRegistration.scss';
import { AuthenticationContext } from '../AuthenticationContext.js';

export const CredentialsRegistrationContext = React.createContext();

export const CredentialsRegistration = ({ registrationRequest, onSuccess }) => {
  const { setRefreshToken } = useContext(AuthenticationContext);
  const [takenUsernames, setTakenUsernames] = useState([]);
  const [alert, setAlert] = useState(null);
  const { t } = useTranslation();
  const history = useHistory();
  const email = registrationRequest ? registrationRequest.email : '';

  const submit = async credentials => {
    const response = await new AuthenticationService().postRegistration(registrationRequest.token, credentials);
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
  };

  return (
    <CredentialsRegistrationContext.Provider value={{ email, takenUsernames, submit }}>
      <div className='credentials-registration'>
        <PageHeading>{t('Registration')}</PageHeading>
        <p>{t('registration-form-instructions')}</p>
        {alert && <Alert type={alert.category} message={alert.message} />}
        <CredentialsRegistrationForm />
      </div>
    </CredentialsRegistrationContext.Provider>
  );
};
