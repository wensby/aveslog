export default class AccountService {

  async fetchAccount(accessToken, username) {
    return await fetch(`${window._env_.API_URL}/accounts/${username}`, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
  }

  async fetchAccounts(accessToken) {
    const url = `${window._env_.API_URL}/accounts?embed=birder`;
    return await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
  }

  async fetchAuthenticatedAccount(accessToken) {
    const url = `${window._env_.API_URL}/account`;
    return await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
  }
}
