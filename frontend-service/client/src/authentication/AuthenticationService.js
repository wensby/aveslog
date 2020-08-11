import axios from 'axios';

export default class AuthenticationService {

  async createCredentialsRecovery(email) {
    return await axios.post(`/api/authentication/credentials-recovery`, {
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
}
