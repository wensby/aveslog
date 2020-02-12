import React, { useState, useEffect } from 'react';
import AccountService from '../account/AccountService.js';
import AuthenticationService from './AuthenticationService.js';

const accountService = new AccountService()
const UserContext = React.createContext();
const refreshTokenKey = 'refreshToken';

const UserProvider = ({ children }) => {
  const [loadingSession, setLoadingSession] = useState(true);
  const [refreshToken, setRefreshToken] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [account, setAccount] = useState(null);

  useEffect(() => {
    const localStorageRefreshToken = localStorage.getItem(refreshTokenKey);
    if (localStorageRefreshToken) {
      setRefreshToken(JSON.parse(localStorageRefreshToken));
    }
    else {
      setLoadingSession(false);
    }
  }, []);

  useEffect(() => {
    if (refreshToken) {
      localStorage.setItem(refreshTokenKey, JSON.stringify(refreshToken));
    }
    else if (!loadingSession) {
      localStorage.removeItem(refreshTokenKey);
    }
  }, [refreshToken, loadingSession]);

  useEffect(() => {
    const resolveAccessToken = async () => {
      const accessToken = await (new AuthenticationService().fetchAccessToken(refreshToken));
      if (accessToken) {
        setAccessToken(accessToken);
      }
      else {
        setRefreshToken(null);
        localStorage.removeItem(refreshTokenKey);
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
        setLoadingSession(false);
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

  if (loadingSession) {
    return null;
  }
  return (
    <UserContext.Provider value={{
      authenticated: refreshToken,
      account,
      unauthenticate,
      setRefreshToken,
      getAccessToken,
    }}>
      {children}
    </UserContext.Provider>
  );
}

export { UserProvider, UserContext }
