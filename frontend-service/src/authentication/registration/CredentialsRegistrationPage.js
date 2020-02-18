import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { useReactRouter } from '../../reactRouterHook';
import AuthenticationService from '../AuthenticationService.js';
import { CredentialsForm } from './CredentialsForm';
import { RegistrationSuccess } from './RegistrationSuccess';
import { FadeIn } from '../../component/FadeIn.js';
import { UserContext } from '../UserContext.js';
import { useHistory } from "react-router-dom";
import { PageHeading } from '../../PageHeading';

export function CredentialsRegistrationPage() {
  const { match } = useReactRouter();
  const history = useHistory();
  const token = match.params.token;
  const [alert, setAlert] = useState(null);
  const [email, setEmail] = useState('');
  const [success, setSuccess] = useState(false);
  const [takenUsernames, setTakenUsernames] = useState([]);
  const { setRefreshToken } = useContext(UserContext);

  const { t } = useTranslation();
  const authentication = new AuthenticationService();

  useEffect(() => {
    const fetchEmail = async () => {
      const response = await new AuthenticationService().fetchRegistration(token);
      if (response.status === 200) {
        const json = await response.json();
        setEmail(json['email']);
      }
    }
    fetchEmail();
  }, [token]);

  const renderAlert = () => {
    if (alert) {
      return (
        <div className='row'>
          <div className={`col alert alert-${alert.category}`} role='alert'>
            { alert.message }
          </div>
        </div>
      );
    }
  }

  const handleFormSubmit = async credentials => {
    try {
      const response = await authentication.postRegistration(token, credentials);
      if (response.status === 201) {
        setSuccess(true);
        const response = await authentication.postRefreshToken(credentials[0], credentials[1]);
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
    <div className='container'>
      <div className='row'>
        <div className='col'>
          <PageHeading>{ t('Registration') }</PageHeading>
          <p>
            { t('registration-form-instructions') }
          </p>
        </div>
      </div>
      {renderAlert()}
      <div className='row'>
        <div className='col'>
          <CredentialsForm
            email={email}
            onSubmit={handleFormSubmit}
            takenUsernames={takenUsernames} />
        </div>
      </div>
    </div>
  );
}
