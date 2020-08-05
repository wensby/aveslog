import React, { useState, useEffect, useRef, useCallback } from 'react';
import AuthenticationService from './AuthenticationService.js';
import axios from 'axios';

const AuthenticationContext = React.createContext();
const refreshTokenKey = 'refreshToken';

const AuthenticationProvider = ({ children }) => {
  const [loading, setLoading] = useState(true);
  const [refreshToken, setRefreshToken] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
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
      // retrieve accessToken upon new refreshToken
      axios.get('/api/authentication/access-token', {
        headers: {
          'refreshToken': refreshToken.jwt,
        }
      })
        .then(response => createAccessToken(response.data))
        .then(freshAccessToken => setAccessToken(freshAccessToken))
        .catch(error => setRefreshToken(null));
      const refreshTokenInterceptor = axios.interceptors.response.use(undefined,
        error => {
          if (error.response) {
            console.log('intercepting axios error response');
            if (error.response.status === 401) {
              if (error.config.url.endsWith('/api/authentication/access-token')) {
                setRefreshToken(null);
                return Promise.reject(error);
              }
              else if (!error.config._retry) {
                error.config._retry = true;
                return axios.get('/api/authentication/access-token', {
                  headers: {
                    'refreshToken': refreshToken.jwt,
                  }
                })
                  .then(response => createAccessToken(response.data))
                  .then(accessToken => {
                    console.log('Received fresh access token');
                    setAccessToken(accessToken);
                    error.config.headers['accessToken'] = accessToken.jwt;
                    return axios(error.config);
                  });
              }
            }
          }
          return Promise.reject(error);
        }
      );
      console.log('Storing refresh token in local storage');
      localStorage.setItem(refreshTokenKey, JSON.stringify(refreshToken));
      return () => {
        axios.interceptors.response.eject(refreshTokenInterceptor);
        console.log('Clearing refresh token from local storage');
        localStorage.removeItem(refreshTokenKey);
        setAccessToken(null);
        setAuthenticated(false);
      };
    }
  }, [refreshToken]);

  useEffect(() => {
    if (accessToken) {
      console.log('got new access token');
      setAuthenticated(true);
      const requestAuthenticationInterceptor = axios.interceptors.request.use(config => {
        if (!config._retry) {
          // When request is a retry, refreshed access token is set by response interceptor
          config.headers['accessToken'] = accessToken.jwt;
        }
        return config;
      });
      return () => axios.interceptors.request.eject(requestAuthenticationInterceptor);
    }
  }, [accessToken]);

  const unauthenticate = useCallback(() => {
    if (refreshToken) {
      axios.delete(`/api/authentication/refresh-token/${refreshToken.id}`)
        .then(__ => setRefreshToken(null));
    }
  }, [refreshToken]);

  const contextValues = {
    authenticated,
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

export { AuthenticationContext, AuthenticationProvider }
