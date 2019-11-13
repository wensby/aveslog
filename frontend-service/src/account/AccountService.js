export default class AccountService {

  async fetchAccounts(accessToken) {
    const url = `${window._env_.API_URL}/accounts`;
    return await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
  }

  async fetchAccount(accessToken) {
    const url = `${window._env_.API_URL}/account`;
    return await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
  }
}
