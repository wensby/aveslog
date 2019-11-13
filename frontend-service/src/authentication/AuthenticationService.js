export default class AuthenticationService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async postRefreshToken(username, password) {
    const url = `${this.apiUrl}/authentication/refresh-token`;
    const parameters = `?username=${username}&password=${password}`;
    return await fetch(url + parameters, {
      method: 'POST',
    });
  }

  async deleteRefreshToken(refreshToken, accessToken) {
    const url = `${this.apiUrl}/authentication/refresh-token/${refreshToken.id}`
    return await fetch(url, {
      method: 'DELETE',
      headers: {
        'accessToken': accessToken.jwt,
      },
    });
  }

  async getAccessToken(refreshToken) {
    return await fetch(`${this.apiUrl}/authentication/access-token`, {
      headers: {
        'refreshToken': refreshToken,
      },
    });
  }

  async postPasswordResetEmail(email) {
    return await fetch(
      `${this.apiUrl}/authentication/password-reset`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          'email': email,
        }),
      }
    );
  }

  async postPasswordResetPassword(token, password) {
    return await fetch(
      `${this.apiUrl}/authentication/password-reset/${token}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          'password': password
        })
      }
    );
  }

  async postPasswordUpdate(accessToken, oldPassword, newPassword) {
    return await fetch(`${this.apiUrl}/authentication/password`, {
      method: 'POST',
      headers: {
        'accessToken': accessToken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'oldPassword': oldPassword,
        'newPassword': newPassword,
      }),
    });
  }

  async postRegistrationEmail(email) {
    const url = `${this.apiUrl}/registration-requests`;
    return await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'email': email,
      })
    });
  }

  async fetchRegistration(token) {
    try {
      const url = `${this.apiUrl}/registration-requests/${token}`;
      return await fetch(url);
    }
    catch (err) {
      return undefined;
    }
  }

  async postRegistration(token, [username, password]) {
    try {
      const url = `${this.apiUrl}/authentication/registration/${token}`;
      return await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          'username': username,
          'password': password,
        })
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
