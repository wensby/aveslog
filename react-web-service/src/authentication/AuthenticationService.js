export default class AuthenticationService {

  async get_authentication_token(username, password) {
    const url = `${window._env_.API_URL}/v2/authentication/token`;
    const parameters = `?username=${username}&password=${password}`;
    const response = await fetch(url + parameters);
    return await response.json();
  }

  async post_password_reset(email) {
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

  async post_registration_email(email) {
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
