class BirderService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  fetchBirder(birderId, accessToken) {
    return fetch(`${window._env_.API_URL}/birders/${birderId}`, {
      headers: {
        'accessToken': accessToken.jwt,
      },
    })
  }
}
const birderService = new BirderService();
export default birderService;
