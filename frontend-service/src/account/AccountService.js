export default class AccountService {

  async fetchAccounts(authToken) {
    const url = `${window._env_.API_URL}/account`;
    const response = await fetch(url, {
      'headers': {
        'authToken': authToken
      }
    });
    const jsonResponse = await response.json();
    return jsonResponse.result;
  }

  async fetchAccount(authToken) {
    const url = `${window._env_.API_URL}/account/me`;
    const response = await fetch(url, {
      'headers': {
        'authToken': authToken
      }
    });
    const jsonResponse = await response.json();
    return jsonResponse.account;
  }
}
