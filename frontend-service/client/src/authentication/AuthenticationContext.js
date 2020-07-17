import React, { useState, useEffect, useRef, useCallback } from 'react';
import AuthenticationService from './AuthenticationService.js';

const AuthenticationContext = React.createContext();
const refreshTokenKey = 'refreshToken';

const AuthenticationProvider = ({ children }) => {
  const [loading, setLoading] = useState(true);
  const [refreshToken, setRefreshToken] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const latestRefreshToken = useRef(refreshToken);
  const [accessTokenPromise, setAccessTokenPromise] = useState(null);
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
        setAccessToken(null);
      }
    }
  }, [refreshToken]);

  const unauthenticate = useCallback(() => {
    if (refreshToken) {
      if (accessToken) {
        new AuthenticationService().deleteRefreshToken(refreshToken, accessToken);
      }
      setRefreshToken(null);
    }
  }, [refreshToken, accessToken]);

  const fetchAccessToken = useCallback(() => {
    console.log('Fetching new access token');
    return fetch('/api/authentication/access-token', {
      headers: {
        'refreshToken': refreshToken.jwt,
      },
    })
      .then(response => {
        if (!response.ok) {
          throw response.status;
        }
        return response;
      })
      .then(response => response.json())
      .then(json => {
        console.log('Received fresh access token');
        return Promise.resolve(createAccessToken(json));
      })
      .catch(error => {
        if (error === 401) {
          setRefreshToken(null);
        }
      });
  }, [refreshToken])

  useEffect(() => {
    const resolveAccessToken = async () => {
      const token = await accessTokenPromise;
      console.log('access token resolved');
      setAccessToken(token);
    }
    if (accessTokenPromise) {
      resolveAccessToken();
    }
  }, [accessTokenPromise]);

  const getAccessToken = useCallback(async () => {
    if (accessToken && new Date() < accessToken.expiration) {
      return accessToken;
    }
    else if (refreshToken) {
      const promise = fetchAccessToken();
      setAccessTokenPromise(promise);
      return await promise;
    }
  }, [accessToken, fetchAccessToken, refreshToken]);

  useEffect(() => {
    if (refreshToken) {
      const promise = fetchAccessToken();
      setAccessTokenPromise(promise);
    }
  }, [refreshToken, fetchAccessToken]);

  const contextValues = {
    authenticated: refreshToken !== null,
    getAccessToken,
    unauthenticate,
    setRefreshToken
  };

  const resolvingAuthentication = (refreshToken && !accessToken) || loading

  return (
    <AuthenticationContext.Provider value={contextValues}>
      {!resolvingAuthentication && children}
    </AuthenticationContext.Provider>
  );
}

const createAccessToken = json => {
  return {
    jwt: json.jwt,
    expiration: createFutureDate(json.expiresIn - 60)
  };
};

const createFutureDate = seconds => {
  const date = new Date();
  date.setSeconds(date.getSeconds() + seconds);
  return date;
};

const status = response => {
  if (response.status === 200) {
    return Promise.resolve(response);
  }
  else if (response.status === 401) {
    return Promise.reject(new Error(response.status));
  }
};

export { AuthenticationContext, AuthenticationProvider }
