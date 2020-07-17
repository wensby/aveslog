import React, { useState } from 'react';
import { useReactRouter } from '../reactRouterHook';
import { RegistrationSuccess } from '../authentication/registration/RegistrationSuccess';
import { FadeIn } from '../component/FadeIn.js';
import { useHistory } from "react-router-dom";
import { useRegistrationRequest } from '../authentication/AuthenticationHooks.js';
import { CredentialsRegistration } from '../authentication/registration/CredentialsRegistration';
import { LoadingOverlay } from '../loading/LoadingOverlay.js';

export default () => {
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
  else if (success) {
    return <FadeIn><RegistrationSuccess /></FadeIn>;
  }
  else if (!registrationRequest) {
    return <LoadingOverlay />;
  }
  else {
    return <CredentialsRegistration
      registrationRequest={registrationRequest}
      onSuccess={handleSuccess} />;
  }
};

