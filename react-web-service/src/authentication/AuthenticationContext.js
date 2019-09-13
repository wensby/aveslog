import React, { useState, useEffect } from 'react';
import AccountService from '../account/AccountService.js';

const accountService = new AccountService()
const AuthenticationContext = React.createContext();

function AuthenticationProvider(props) {
  const [authenticated, setAuthenticated] = useState(false);
  const [account, setAccount] = useState(null);
  const [token, setToken] = useState(null);

  const resolveLocalStorageToken = async () => {
    const localStorageToken = localStorage.getItem('authenticationToken');
    if (authenticated && !localStorageToken) {
      setToken(null);
      setAuthenticated(false);
      setAccount(false);
    }
    else if (!authenticated && localStorageToken) {
      setToken(localStorageToken);
      setAuthenticated(true);
      const account = await accountService.fetchAccount(localStorageToken);
      setAccount(account);
    }
  }

  useEffect(() => {
    resolveLocalStorageToken();
  });
  
  const onAuthenticated = async token => {
    setToken(token);
    localStorage.setItem('authenticationToken', token);
    setAuthenticated(true);
    const account = await accountService.fetchAccount(token);
    setAccount(account);
  }

  const unauthenticate = () => {
    setToken(null);
    setAuthenticated(false);
    setAccount(false);
    localStorage.removeItem('authenticationToken');
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

export { AuthenticationProvider, AuthenticationContext }
