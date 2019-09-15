import React, { useState, useEffect } from 'react';
import AccountService from '../account/AccountService.js';

const accountService = new AccountService()
const AuthenticationContext = React.createContext();

function AuthenticationProvider(props) {
  const [authenticated, setAuthenticated] = useState(false);
  const [account, setAccount] = useState(null);
  const [token, setToken] = useState(null);
  const [resolvingLocalStorage, setResolvingLocalStorage] = useState(true);

  const resolveLocalStorageToken = async () => {
    const localStorageToken = localStorage.getItem('authenticationToken');
    if (authenticated && !localStorageToken) {
      setToken(null);
      setAuthenticated(false);
      setAccount(null);
    }
    else if (!authenticated && localStorageToken) {
      const account = await accountService.fetchAccount(localStorageToken);
      if (account) {
        setToken(localStorageToken);
        setAuthenticated(true);
        setAccount(account);
      }
      else {
        setToken(null);
        setAuthenticated(false);
        setAccount(null);
        localStorage.removeItem('authenticationToken');
      }
    }
    setResolvingLocalStorage(false);
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

  if (resolvingLocalStorage) {
    return null;
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
