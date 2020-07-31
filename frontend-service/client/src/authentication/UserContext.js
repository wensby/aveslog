import React, { useState, useEffect, useContext } from 'react';
import { AuthenticationContext } from './AuthenticationContext.js';
import axios from 'axios';

const UserContext = React.createContext();

const UserProvider = ({ children }) => {
  const { authenticated } = useContext(AuthenticationContext);
  const [account, setAccount] = useState(null);

  useEffect(() => {
    if (authenticated) {
      console.log('fetching account');
      axios.get('/api/account')
        .then(response => setAccount(response.data));
    }
    else {
      setAccount(null);
    }
  }, [authenticated]);

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
