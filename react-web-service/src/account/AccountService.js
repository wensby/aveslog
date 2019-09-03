export default class AccountService {

  async fetchAccount(authToken) {
    const url = `${window._env_.API_URL}/v2/account/me`;
    const response = await fetch(url, {
      'headers': {
        'authToken': authToken
      }
    });
    const jsonResponse = await response.json();
    return jsonResponse.account;
  }
}
