import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const AuthenticationContext = React.createContext();
const refreshTokenKey = 'refreshToken';

const AuthenticationProvider = ({ children }) => {
  const [loading, setLoading] = useState(true);
  const [refreshToken, setRefreshToken] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    const localStorageRefreshToken = localStorage.getItem(refreshTokenKey);
    if (localStorageRefreshToken) {
      console.log('Recovered local storage refresh token');
      const refreshToken = JSON.parse(localStorageRefreshToken);
      axios.post('/api/authentication/access-token', {
        refreshToken: refreshToken.jwt,
      })
        .then(response => createAccessToken(response.data))
        .then(accessToken => {
          console.log('Received access token with refresh token recovered from local storage');
          setRefreshToken(refreshToken);
          setAccessToken(accessToken);
        })
        .catch(__ => localStorage.removeItem(refreshTokenKey))
        .finally(() => setLoading(false))
    }
    else {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (refreshToken) {
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
                return axios.post('/api/authentication/access-token', {
                    refreshToken: refreshToken.jwt,
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
    else {
      setAuthenticated(false);
    }
  }, [accessToken]);

  const unauthenticate = useCallback(() => {
    if (refreshToken) {
      axios.delete(`/api/authentication/refresh-token/${refreshToken.id}`)
        .then(__ => setRefreshToken(null));
    }
  }, [refreshToken]);

  const login = (username, password) => {
    return axios.post('/api/authentication/tokens', {
      username: username.toLowerCase(),
      password: password,
    }).then(response => {
      setRefreshToken(createRefreshToken(response.data.refreshToken));
      setAccessToken(createAccessToken(response.data.accessToken));
      return true;
    }).catch(__ => Promise.reject(false));
  }

  const contextValues = {
    authenticated,
    unauthenticate,
    login
  };

  return (
    <AuthenticationContext.Provider value={contextValues}>
      {!loading && children}
    </AuthenticationContext.Provider>
  );
}

const createAccessToken = json => {
  return {
    jwt: json.jwt,
    expiration: createFutureDate(json.expiresIn - 60)
  };
};

const createRefreshToken = json => {
  return {
    id: json.id,
    jwt: json.refreshToken,
    expiration: Date.parse(json.expirationDate),
  }
}

const createFutureDate = seconds => {
  const date = new Date();
  date.setSeconds(date.getSeconds() + seconds);
  return date;
};

export { AuthenticationContext, AuthenticationProvider }
