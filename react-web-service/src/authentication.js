export default class Authentication {

  async login(username, password) {
    const url = `${window._env_.API_URL}/v2/authentication/token`
      + `?username=${username}&password=${password}`
    const response = await fetch(url);
    const jsonResponse = await response.json();
    localStorage.setItem('authToken', jsonResponse.authToken);
  }

  async logout() {
    localStorage.removeItem('authToken');
  }
}