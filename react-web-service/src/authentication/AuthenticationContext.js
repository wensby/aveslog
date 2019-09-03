import React, { useState } from 'react';
import AccountService from '../account/AccountService.js';

const accountService = new AccountService()
const AuthenticationContext = React.createContext();

function AuthenticationProvider(props) {
  const [authenticated, setAuthenticated] = useState(false);
  const [account, setAccount] = useState(null);
  const [token, setToken] = useState(null);
  
  const onAuthenticated = async token => {
    setToken(token);
    setAuthenticated(true);
    const account = await accountService.fetchAccount(token);
    setAccount(account);
  }

  const unauthenticate = () => {
    setToken(null);
    setAuthenticated(false);
    setAccount(false);
  }

  return (
    <AuthenticationContext.Provider value={{
      authenticated: authenticated,
      account: account,
      onAuthenticated: onAuthenticated,
      unauthenticate: unauthenticate,
      token: token,
    }}>
      {props.children}
    </AuthenticationContext.Provider>
  );
}

const AuthenticationConsumer = AuthenticationContext.Consumer;

export { AuthenticationProvider, AuthenticationConsumer, AuthenticationContext }
