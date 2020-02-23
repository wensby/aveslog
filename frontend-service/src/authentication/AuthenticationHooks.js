import { useState, useEffect, useContext } from 'react';
import { UserContext } from './UserContext.js';
import AuthenticationService from './AuthenticationService.js';

export function useAuthentication() {
  const { authenticated, account } = useContext(UserContext);
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
};
