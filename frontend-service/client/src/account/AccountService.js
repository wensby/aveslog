export default class AccountService {

  async fetchAccount(accessToken, username) {
    return await fetch(`/api/accounts/${username}`, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
  }

  async fetchAccounts(accessToken) {
    const url = `/api/accounts?embed=birder`;
    return await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
  }

  async fetchAuthenticatedAccount(accessToken) {
    const url = `/api/account`;
    return await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt
      }
    });
  }
}
