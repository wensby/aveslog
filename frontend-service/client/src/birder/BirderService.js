class BirderService {

  fetchBirder(birderId, accessToken) {
    return fetch(`/api/birders/${birderId}`, {
      headers: {
        'accessToken': accessToken.jwt,
      },
    })
  }
}
const birderService = new BirderService();
export default birderService;
