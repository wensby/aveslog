import { useState, useEffect, useContext } from 'react';
import { UserContext } from './UserContext.js';
import AuthenticationService from './AuthenticationService.js';
import { AuthenticationContext } from './AuthenticationContext.js';

export function useAuthentication() {
  const { account } = useContext(UserContext);
  const { authenticated } = useContext(AuthenticationContext);
  if (authenticated) {
    return { account };
  }
  return { };
}

export const useRegistrationRequest = token => {
  const [registrationRequest, setRegistrationRequest] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const resolveRegistrationRequest = async () => {
      const response = await new AuthenticationService().fetchRegistration(token);
      if (response.status === 200) {
        setRegistrationRequest(response.data);
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
};
