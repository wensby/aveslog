import axios from 'axios';

export default class AuthenticationService {

  postRefreshToken(username, password) {
    const url = '/api/authentication/refresh-token';
    const parameters = `?username=${username.toLowerCase()}&password=${password}`;
    return axios.post(url + parameters);
  }

  async deleteRefreshToken(refreshToken) {
    return await axios.delete(`/api/authentication/refresh-token/${refreshToken.id}`);
  }

  async postPasswordResetEmail(email) {
    return await axios.post(`/api/authentication/password-reset`, {
      'email': email,
    });
  }

  async postPasswordResetPassword(token, password) {
    return await axios.post(`/api/authentication/password-reset/${token}`,
      {
        'password': password
      });
  }

  async postPasswordUpdate(oldPassword, newPassword) {
    return await axios.post('/api/account/password', {
      'oldPassword': oldPassword,
      'newPassword': newPassword,
    });
  }

  async postRegistrationEmail(email, locale) {
    return await axios.post('/api/registration-requests',
      {
        'email': email,
        'locale': locale
      });
  }

  async fetchRegistration(token) {
    try {
      return await axios.get(`/api/registration-requests/${token}`);
    }
    catch (err) {
      return undefined;
    }
  }

  async postRegistration(token, [username, password]) {
    try {
      return await axios.post('/api/accounts',
        {
          'token': token,
          'username': username,
          'password': password,
        });
    }
    catch (err) {
      return undefined;
    }
  }

  async logout() {
    localStorage.removeItem('accessToken');
  }
}
