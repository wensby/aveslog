export default class AuthenticationService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async fetchAuthenticationToken(username, password) {
    const url = `${window._env_.API_URL}/v2/authentication/token`;
    const parameters = `?username=${username}&password=${password}`;
    const response = await fetch(url + parameters);
    return await response.json();
  }

  async postPasswordResetEmail(email) {
    const response = await fetch(
      `${window._env_.API_URL}/v2/authentication/password-reset`,
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
    return await response.json();
  }

  async postPasswordResetPassword(token, password) {
    const response = await fetch(
      `${this.apiUrl}/v2/authentication/password-reset/${token}`,
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
    return await response.json();
  }

  async postRegistrationEmail(email) {
    const url = `${window._env_.API_URL}/v2/authentication/registration`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'email': email,
      })
    })
    return await response.json();
  }

  async logout() {
    localStorage.removeItem('authToken');
  }
}
