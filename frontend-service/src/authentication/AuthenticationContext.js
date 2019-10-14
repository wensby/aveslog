import React, { useState, useEffect } from 'react';
import AccountService from '../account/AccountService.js';
import AuthenticationService from './AuthenticationService.js';

const accountService = new AccountService()
const AuthenticationContext = React.createContext();

function AuthenticationProvider(props) {
  const [refreshToken, setRefreshToken] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [account, setAccount] = useState(null);
  const [resolvingLocalStorage, setResolvingLocalStorage] = useState(true);
  const authenticationService = new AuthenticationService();

  useEffect(() => {
    const localStorageRefreshToken = localStorage.getItem('refreshTokenJwt');
    const localStorageRefreshTokenExp = localStorage.getItem('refreshTokenExpiration');
    const localStorageRefreshTokenId = localStorage.getItem('refreshTokenId');
    if (localStorageRefreshToken && localStorageRefreshTokenExp && localStorageRefreshTokenId) {
      console.log('Refresh token recovered from local storage.');
      setRefreshToken({
        id: localStorageRefreshTokenId,
        jwt: localStorageRefreshToken,
        expiration: localStorageRefreshTokenExp,
      });
    }
    else {
      setResolvingLocalStorage(false);
    }
  }, []);

  useEffect(() => {
    if (refreshToken) {
      console.log('storing refresh token in storage');
      localStorage.setItem('refreshTokenJwt', refreshToken.jwt);
      localStorage.setItem('refreshTokenExpiration', refreshToken.expiration);
      localStorage.setItem('refreshTokenId', refreshToken.id);
    }
    else {
      console.log('clearing refresh token from storage');
      localStorage.removeItem('refreshTokenJwt');
      localStorage.removeItem('refreshTokenExpiration');
      localStorage.removeItem('refreshTokenId');
    }
  }, [refreshToken]);

  useEffect(() => {
    if (refreshToken) {
      resolveAccessToken();
    }
  }, [refreshToken]);

  async function fetchAccount(accessToken) {
    if (accessToken) {
      setAccount(await accountService.fetchAccount(accessToken));
      setResolvingLocalStorage(false);
    }
  }

  useEffect(() => {
    fetchAccount(accessToken);
  }, [accessToken]);

  const fetchAccessToken = async refreshToken => {
    console.log('fetching access token');
    const response = await authenticationService.getAccessToken(refreshToken.jwt);
    if (response.status === 200) {
      const json = await response.json();
      return { jwt: json.accessToken, expiration: json.expirationDate };
    }
    return null;
  }

  const resolveAccessToken = async () => {
    const accessToken = await fetchAccessToken(refreshToken);
    if (accessToken) {
      setAccessToken(accessToken);
    }
    else {
      setRefreshToken(null);
    }
  }

  const asyncUnauthenticate = async () => {
    const accessToken = await getAccessToken();
    const response = await authenticationService.deleteRefreshToken(refreshToken, accessToken);
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

  const currentUtcTime = () => {
    const date = new Date();
    return Date.UTC(
      date.getUTCFullYear(),
      date.getUTCMonth(),
      date.getUTCDate(),
      date.getUTCHours(),
      date.getUTCMinutes(),
      date.getUTCSeconds());
  }

  const getAccessToken = async () => {
    const currentTime = currentUtcTime();
    const tenSeconds = 10000;
    if (!accessToken || accessToken.expiration > currentTime + tenSeconds) {
      console.log("access token need refreshing");
      const accessToken = await fetchAccessToken(refreshToken);
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
    <AuthenticationContext.Provider value={{
      authenticated: refreshToken,
      account,
      unauthenticate,
      refreshToken,
      setRefreshToken,
      setAccessToken,
      getAccessToken,
    }}>
      {props.children}
    </AuthenticationContext.Provider>
  );
}

export { AuthenticationProvider, AuthenticationContext }
