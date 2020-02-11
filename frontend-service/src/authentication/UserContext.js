import React, { useState, useEffect } from 'react';
import AccountService from '../account/AccountService.js';
import AuthenticationService from './AuthenticationService.js';

const accountService = new AccountService()
const UserContext = React.createContext();

function UserProvider(props) {
  const [resolvingLocalStorage, setResolvingLocalStorage] = useState(true);
  const [refreshToken, setRefreshToken] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [account, setAccount] = useState(null);

  useEffect(() => {
    const localStorageRefreshToken = localStorage.getItem('refreshToken');
    if (localStorageRefreshToken) {
      console.log('Refresh token recovered from local storage.');
      setRefreshToken(JSON.parse(localStorageRefreshToken));
    }
    else {
      console.log('No refresh token found in local storage.');
      setResolvingLocalStorage(false);
    }
  }, []);

  useEffect(() => {
    if (refreshToken) {
      console.log('storing refresh token in storage');
      localStorage.setItem('refreshToken', JSON.stringify(refreshToken));
    }
    else if (!resolvingLocalStorage) {
      console.log('clearing refresh token from storage');
      localStorage.removeItem('refreshToken');
    }
  }, [refreshToken, resolvingLocalStorage]);

  useEffect(() => {
    const resolveAccessToken = async () => {
      const accessToken = await (new AuthenticationService().fetchAccessToken(refreshToken));
      if (accessToken) {
        setAccessToken(accessToken);
      }
      else {
        setRefreshToken(null);
        localStorage.removeItem('refreshToken');
      }
    }
    if (refreshToken) {
      resolveAccessToken();
    }
  }, [refreshToken]);

  useEffect(() => {
    const fetchAccount = async accessToken => {
      const response = await accountService.fetchAuthenticatedAccount(accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setAccount(json);
        setResolvingLocalStorage(false);
      }
    }
    if (accessToken) {
      fetchAccount(accessToken);
    }
  }, [accessToken]);

  const asyncUnauthenticate = async () => {
    const accessToken = await getAccessToken();
    const response = await (new AuthenticationService().deleteRefreshToken(refreshToken, accessToken));
    if (response.status === 204) {
      setRefreshToken(null);
      setAccessToken(null);
      setAccount(false);
    }
  }

  const unauthenticate = () => {
    if (refreshToken) {
      asyncUnauthenticate();
    }
  }

  const getAccessToken = async () => {
    const tenSeconds = 10000;
    if (!accessToken || (new Date().getTime() + tenSeconds) > accessToken.expiration) {
      console.log("access token need refreshing");
      const accessToken = await (new AuthenticationService().fetchAccessToken(refreshToken));
      if (accessToken) {
        setAccessToken(accessToken);
        return accessToken;
      }
    }
    else {
      return accessToken;
    }
  }

  if (resolvingLocalStorage) {
    return null;
  }
  return (
    <UserContext.Provider value={{
      authenticated: refreshToken,
      account,
      unauthenticate,
      refreshToken,
      setRefreshToken,
      setAccessToken,
      getAccessToken,
    }}>
      {props.children}
    </UserContext.Provider>
  );
}

export { UserProvider, UserContext }
