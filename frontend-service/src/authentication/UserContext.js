import React, { useState, useEffect, useRef, useCallback } from 'react';
import AuthenticationService from './AuthenticationService.js';

const UserContext = React.createContext();
const refreshTokenKey = 'refreshToken';

const createAccessToken = json => {
  return { jwt: json.jwt, expiration: createFutureDate(json.expiresIn) };
};

const createFutureDate = seconds => {
  const date = new Date();
  date.setSeconds(date.getSeconds() + seconds);
  return date;
};

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
    if (refreshToken) {
      console.log('Storing refresh token in local storage');
      localStorage.setItem(refreshTokenKey, JSON.stringify(refreshToken));
      return () => {
        console.log('Clearing refresh token from local storage');
        localStorage.removeItem(refreshTokenKey);
      }
    }
  }, [refreshToken]);

  useEffect(() => {
    const refreshAccessToken = async () => {
      if (refreshToken && refreshToken === latestRefreshToken.current) {
        console.log('Refreshing access token');
        const response = await fetchAccessToken(refreshToken);
        if (response.status === 200) {
          console.log('Received fresh access token');
          const json = await response.json();
          const accessToken = createAccessToken(json);
          setAccessToken(accessToken);
          const refreshDeadline = (json.expiresIn - 60) * 1000;
          setTimeout(refreshAccessToken, refreshDeadline);
        }
        else if (response.status === 401) {
          unauthenticate();
        }
      }
    };
    refreshAccessToken();
  }, [refreshToken]);

  useEffect(() => {
    if (!loading && !refreshToken) {
      unauthenticate();
    }
  }, [loading, refreshToken]);

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

  const unauthenticate = useCallback(async () => {
    if (refreshToken) {
      if (accessToken) {
        await (new AuthenticationService().deleteRefreshToken(refreshToken, accessToken));
      }
      setRefreshToken(null);
      setAccessToken(null);
      setAccount(null);
    }
  }, [refreshToken, accessToken]); 

  const unresolvedAccount = refreshToken && !account;
  const accessTokenExpired = accessToken && accessToken.expiration < new Date();

  const getAccessToken = useCallback(() => {
    if (accessToken && new Date() < accessToken.expiration) {
      return accessToken;
    }
    else {
      return null;
    }
  }, [accessToken]);

  if (loading || unresolvedAccount || accessTokenExpired) {
    return null;
  }

  const contextValues = {
    authenticated: accessToken !== null,
    getAccessToken,
    account,
    unauthenticate,
    setRefreshToken
  };

  return (
    <UserContext.Provider value={contextValues}>
      {children}
    </UserContext.Provider>
  );
}

export { UserProvider, UserContext }
