import React, { useState, useEffect } from 'react';
import AccountService from '../account/AccountService.js';
import AuthenticationService from './AuthenticationService.js';

const accountService = new AccountService()
const UserContext = React.createContext();

function UserProvider(props) {
  const [refreshToken, setRefreshToken] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [account, setAccount] = useState(null);
  const [resolvingLocalStorage, setResolvingLocalStorage] = useState(true);

  useEffect(() => {
    const localStorageRefreshToken = localStorage.getItem('refreshToken');
    if (localStorageRefreshToken) {
      console.log('Refresh token recovered from local storage.');
      setRefreshToken(JSON.parse(localStorageRefreshToken));
    }
    else {
      setResolvingLocalStorage(false);
    }
  }, []);

  useEffect(() => {
    if (refreshToken) {
      console.log('storing refresh token in storage');
      localStorage.setItem('refreshToken', JSON.stringify(refreshToken));
    }
    else {
      console.log('clearing refresh token from storage');
      localStorage.removeItem('refreshToken');
    }
  }, [refreshToken]);

  useEffect(() => {
    const resolveAccessToken = async () => {
      const accessToken = await (new AuthenticationService().fetchAccessToken(refreshToken));
      if (accessToken) {
        setAccessToken(accessToken);
      }
      else {
        setRefreshToken(null);
      }
    }
    if (refreshToken) {
      resolveAccessToken();
    }
  }, [refreshToken]);

  const fetchAccount = async accessToken => {
    if (accessToken) {
      const response = await accountService.fetchAuthenticatedAccount(accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setAccount(json);
        setResolvingLocalStorage(false);
      }
    }
  }
  
  useEffect(() => {
    console.log(`new access token: ${JSON.stringify(accessToken)}`)
    fetchAccount(accessToken);
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
      console.log("access token doesn't need refreshing");
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
