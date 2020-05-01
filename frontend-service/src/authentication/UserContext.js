import React, { useState, useEffect, useContext } from 'react';
import { AuthenticationContext } from './AuthenticationContext.js';

const UserContext = React.createContext();

const UserProvider = ({ children }) => {
  const { authenticated, getAccessToken } = useContext(AuthenticationContext);
  const [account, setAccount] = useState(null);
  
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
      const accessToken = await getAccessToken();
      const response = await fetchAuthenticatedAccount(accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setAccount(json);
      }
    };
    if (authenticated) {
      resolveAccount();
    }
    else {
      setAccount(null);
    }
  }, [authenticated, getAccessToken]);

  if (authenticated && !account) {
    return null;
  }

  const patchBirder = birder => {
    setAccount(prevAccount => {
      return { ...prevAccount, birder: birder };
    })
  };

  const contextValues = { account, patchBirder };

  return (
    <UserContext.Provider value={contextValues}>
      {children}
    </UserContext.Provider>
  );
}

export { UserProvider, UserContext }
