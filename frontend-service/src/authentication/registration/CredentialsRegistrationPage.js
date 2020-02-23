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
  const [success, setSuccess] = useState(false);
  const { token } = match.params;
  const { registrationRequest, error } = useRegistrationRequest(token);
  const history = useHistory();

  const handleSuccess = () => {
    setSuccess(true);
  };

  if (error === 404) {
    history.push('/authentication/login');
  }
  if (success) {
    return <FadeIn><RegistrationSuccess /></FadeIn>;
  }
  return <CredentialsRegistration
    token={token}
    registrationRequest={registrationRequest}
    onSuccess={handleSuccess} />;
};

const CredentialsRegistration = ({ token, registrationRequest, onSuccess }) => {
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

const useRegistrationRequest = token => {
  const [registrationRequest, setRegistrationRequest] = useState(null);
  const [error, setError] = useState(null);
  useEffect(() => {
    const resolveRegistrationRequest = async () => {
      const response = await new AuthenticationService().fetchRegistration(token);
      if (response.status === 200) {
        setRegistrationRequest(await response.json());
      }
      else {
        setError(response.status);
      }
    }
    setError(null);
    setRegistrationRequest(null);
    resolveRegistrationRequest();
  }, [token]);
  return { registrationRequest, error };
}
