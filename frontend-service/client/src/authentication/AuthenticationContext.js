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
        .then(freshAccessToken => {
          console.log('Received fresh access token');
          setAccessToken(freshAccessToken);
        });
      const expiredAccessTokenRefresherInterceptor = axios.interceptors.response.use(
        response => response,
        error => {
          console.log('intercepting axios error response');
          if (error.response && error.response.status === 401
            && error.config.url === axios.defaults.baseURL + '/api/authentication/access-token') {
            setRefreshToken(null);
            return Promise.reject(error);
          }
          if (error.response && error.response.status === 401
            && !error.config._retry) {
            error.config._retry = true;
            return axios.get('/api/authentication/access-token', {
              headers: {
                'refreshToken': refreshToken.jwt,
              }
            })
              .then(response => createAccessToken(response.data))
              .then(freshAccessToken => {
                console.log('Received fresh access token');
                setAccessToken(freshAccessToken);
                axios.defaults.headers.common['accessToken'] = freshAccessToken.jwt;
                return axios(error.config);
              })
          }
          return Promise.reject(error);
        }
      );
      console.log('Storing refresh token in local storage');
      localStorage.setItem(refreshTokenKey, JSON.stringify(refreshToken));
      return () => {
        console.log('Clearing refresh token from local storage');
        localStorage.removeItem(refreshTokenKey);
        setAccessToken(null);
        setAuthenticated(false);
        axios.interceptors.response.eject(expiredAccessTokenRefresherInterceptor);
      }
    }
    else {
      setAccessToken(null);
    }
  }, [refreshToken]);

  useEffect(() => {
    if (accessToken) {
      setAuthenticated(true);
      const requestAuthenticationInterceptor = axios.interceptors.request.use(config => {
        config.headers['accessToken'] = accessToken.jwt;
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
