export default class Authentication {

  async get_authentication_token(username, password) {
    const url = `${window._env_.API_URL}/v2/authentication/token`;
    const parameters = `?username=${username}&password=${password}`;
    const response = await fetch(url + parameters);
    return await response.json();
  }

  async post_password_reset(email) {
    return {status: 'failure'};
  }

  async logout() {
    localStorage.removeItem('authToken');
  }
}
