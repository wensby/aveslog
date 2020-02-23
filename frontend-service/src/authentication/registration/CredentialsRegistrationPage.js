import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { useReactRouter } from '../../reactRouterHook';
import AuthenticationService from '../AuthenticationService.js';
import { CredentialsForm } from './CredentialsForm';
import { RegistrationSuccess } from './RegistrationSuccess';
import { FadeIn } from '../../component/FadeIn.js';
import { UserContext } from '../UserContext.js';
import { useHistory } from "react-router-dom";
import { PageHeading } from '../../generic/PageHeading.js';
import { Alert } from '../../generic/Alert';

export const CredentialsRegistrationPage = () => {
  const { match } = useReactRouter();
  const history = useHistory();
  const { token } = match.params;
  const { registrationRequest } = useRegistrationRequest(token);
  const [alert, setAlert] = useState(null);
  const [email, setEmail] = useState('');
  const [success, setSuccess] = useState(false);
  const [takenUsernames, setTakenUsernames] = useState([]);
  const { setRefreshToken } = useContext(UserContext);
  const { t } = useTranslation();

  useEffect(() => {
    if (registrationRequest) {
      setEmail(registrationRequest['email']);
    }
  }, [registrationRequest]);

  const renderAlert = () => {
    if (alert) {
      return (
        <div className='row'>
          <Alert type={alert.category} message={alert.message} />
        </div>
      );
    }
  }

  const handleFormSubmit = async credentials => {
    try {
      const response = await new AuthenticationService().postRegistration(token, credentials);
      if (response.status === 201) {
        setSuccess(true);
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

  if (success) {
    return <FadeIn><RegistrationSuccess /></FadeIn>;
  }
  return (
    <div>
      <PageHeading>{t('Registration')}</PageHeading>
      <p>{t('registration-form-instructions')}</p>
      {renderAlert()}
      <CredentialsForm email={email} onSubmit={handleFormSubmit} takenUsernames={takenUsernames} />
    </div>
  );
};

const useRegistrationRequest = token => {
  const [registrationRequest, setRegistrationRequest] = useState(null);
  useEffect(() => {
    const resolveRegistrationRequest = async () => {
      const response = await new AuthenticationService().fetchRegistration(token);
      if (response.status === 200) {
        setRegistrationRequest(await response.json());
      }
    }
    resolveRegistrationRequest();
  }, [token]);
  return { registrationRequest };
}
