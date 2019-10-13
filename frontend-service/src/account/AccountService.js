export default class AccountService {

  async fetchAccounts(accessToken) {
    const url = `${window._env_.API_URL}/account`;
    const response = await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
    const jsonResponse = await response.json();
    return jsonResponse.result;
  }

  async fetchAccount(accessToken) {
    const url = `${window._env_.API_URL}/account/me`;
    const response = await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
    const jsonResponse = await response.json();
    return jsonResponse.account;
  }
}
