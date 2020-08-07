import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { CredentialsRegistrationForm } from './CredentialsRegistrationForm';
import { useHistory } from "react-router-dom";
import { PageHeading } from '../../generic/PageHeading.js';
import { Alert } from '../../generic/Alert';
import { AuthenticationContext } from '../AuthenticationContext.js';
import axios from 'axios';
import './CredentialsRegistration.scss';

export const CredentialsRegistrationContext = React.createContext();

export const CredentialsRegistration = ({ registrationRequest, onSuccess }) => {
  const { login } = useContext(AuthenticationContext);
  const [takenUsernames, setTakenUsernames] = useState([]);
  const [alert, setAlert] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const { t } = useTranslation();
  const history = useHistory();
  const email = registrationRequest ? registrationRequest.email : '';

  const submit = async credentials => {
    setSubmitting(true);
    axios.post('/api/accounts', {
      'token': registrationRequest.token,
      'username': credentials[0],
      'password': credentials[1],
    })
      .then(__ => login(credentials[0], credentials[1]))
      .then(__ => history.push('/home'))
      .catch(error => {
        if (error.response) {
          if (error.response.status === 409) {
            if (error.response.data['code'] === 3) {
              setTakenUsernames(takenUsernames.concat([credentials[0]]))
              setAlert({
                category: 'danger',
                message: 'Username already taken.',
              });
            }
          }
          else if (error.response.status === 400) {
            setAlert({
              category: 'danger',
              message: 'An error occurred.'
            });
          }
        }
      })
      .finally(() => setSubmitting(false));
  };

  return (
    <CredentialsRegistrationContext.Provider value={{ email, takenUsernames, submit, submitting }}>
      <div className='credentials-registration'>
        <PageHeading>{t('Registration')}</PageHeading>
        <p>{t('registration-form-instructions')}</p>
        {alert && <Alert type={alert.category} message={alert.message} />}
        <CredentialsRegistrationForm />
      </div>
    </CredentialsRegistrationContext.Provider>
  );
};
