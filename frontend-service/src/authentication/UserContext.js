import React, { useState, useEffect, useRef } from 'react';
import AuthenticationService from './AuthenticationService.js';

const UserContext = React.createContext();
const refreshTokenKey = 'refreshToken';

const UserProvider = ({ children }) => {
  const [loading, setLoading] = useState(true);
  const [refreshToken, setRefreshToken] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [account, setAccount] = useState(null);
  const latestRefreshToken = useRef(refreshToken);
  latestRefreshToken.current = refreshToken;

  useEffect(() => {
    const localStorageRefreshToken = localStorage.getItem(refreshTokenKey);
    if (localStorageRefreshToken) {
      console.log('Recovered local storage refresh token');
      setRefreshToken(JSON.parse(localStorageRefreshToken));
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    const refreshAccessToken = async refreshToken => {
      const response = await fetchAccessToken(refreshToken);
      if (response.status === 200) {
        const json = await response.json();
        const accessToken = createAccessToken(json);
        console.log('Resolved new access token');
        setAccessToken(accessToken);
        setTimeout(() => {
          console.log('Access token refresh timeout hit');
          if (latestRefreshToken.current === refreshToken) {
            refreshAccessToken(refreshToken);
          }
        }, (json.expiresIn - 60) * 1000);
      }
      else if (response.status === 401) {
        unauthenticate();
      }
    };
    if (refreshToken) {
      refreshAccessToken(refreshToken);
    }
    else {
      setAccessToken(null);
    }
  }, [refreshToken]);

  useEffect(() => {
    if (!loading) {
      if (refreshToken) {
        localStorage.setItem(refreshTokenKey, JSON.stringify(refreshToken));
      }
      else {
        localStorage.removeItem(refreshTokenKey);
      }
    }

  }, [refreshToken, loading]);

  useEffect(() => {
    if (accessToken) {
      resolveAccount(accessToken);
    }
  }, [accessToken]);

  const resolveAccount = async accessToken => {
    const response = await fetchAuthenticatedAccount(accessToken);
    if (response.status === 200) {
      const json = await response.json();
      setAccount(json);
    }
  };

  const fetchAuthenticatedAccount = async accessToken => {
    const url = `${window._env_.API_URL}/account`;
    return await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
  };

  const fetchAccessToken = async refreshToken => {
    console.log('Fetching new access token');
    return await fetch(`${window._env_.API_URL}/authentication/access-token`, {
      headers: {
        'refreshToken': refreshToken.jwt,
      },
    });
  };

  const unauthenticate = async () => {
    if (refreshToken) {
      const response = await (new AuthenticationService().deleteRefreshToken(refreshToken, accessToken));
      if (response.status === 204) {
        setRefreshToken(null);
        localStorage.removeItem(refreshTokenKey);
        setAccessToken(null);
        setAccount(false);
      }
    }
  };

  const createAccessToken = json => {
    return { jwt: json.jwt, expiration: createFutureDate(json.expiresIn) };
  };

  const createFutureDate = seconds => {
    const date = new Date();
    date.setSeconds(date.getSeconds() + seconds);
    return date;
  };

  if (loading || (refreshToken && !account)) {
    return null;
  }
  return (
    <UserContext.Provider value={{
      authenticated: accessToken !== null,
      account,
      unauthenticate,
      setRefreshToken,
      accessToken,
    }}>
      {children}
    </UserContext.Provider>
  );
}

export { UserProvider, UserContext }
