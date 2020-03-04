import React, { useState, useEffect, useContext } from 'react';
import { AuthenticationContext } from './AuthenticationContext.js';

const UserContext = React.createContext();

const UserProvider = ({ children }) => {
  const { getAccessToken } = useContext(AuthenticationContext);
  const [account, setAccount] = useState(null);
  const accessToken = getAccessToken();
  
  useEffect(() => {
    const resolveAccount = async () => {
      const fetchAuthenticatedAccount = async accessToken => {
        const url = `${window._env_.API_URL}/account`;
        return await fetch(url, {
          'headers': {
            'accessToken': accessToken.jwt
          }
        });
      };
      const response = await fetchAuthenticatedAccount(accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setAccount(json);
      }
    };
    if (accessToken) {
      resolveAccount();
    }
  }, [accessToken]);  

  if (accessToken && !account) {
    return null;
  }

  const contextValues = { account };

  return (
    <UserContext.Provider value={contextValues}>
      {children}
    </UserContext.Provider>
  );
}

export { UserProvider, UserContext }
