import React, { useCallback, useContext } from 'react';
import { AuthenticationContext } from 'authentication/AuthenticationContext';

const ApiContext = React.createContext();

const ApiProvider = ({ children }) => {
  const { authenticated, getAccessToken } = useContext(AuthenticationContext);

  const apiFetch = useCallback((url, options) => {
    const prefixedUrl = `${window._env_.API_URL}${url}`;
    return fetch(prefixedUrl, options);
  }, []);

  const authenticatedApiFetch = useCallback(async (url, options) => {
    if (authenticated) {
      const accessToken = await getAccessToken();
      const extraOptions = {
        headers: {
          'accessToken': accessToken.jwt,
          ...options.headers || {}
        }
      };
      return apiFetch(url, { ...options, ...extraOptions });
    }
    else {
      return apiFetch(url, options);
    }
  }, [getAccessToken]);

  const value = {
    apiFetch,
    authenticatedApiFetch,
  };

  return (
    <ApiContext.Provider value={value}>
      {children}
    </ApiContext.Provider>
  );
}

export { ApiContext, ApiProvider }
