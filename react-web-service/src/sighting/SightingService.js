export default class SightingService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async fetchSightings(username, authToken) {
    const url = `${this.apiUrl}/v2/profile/${username}/sighting`;
    const response = await fetch(url, {
      'headers': {
        'authToken': authToken,
      },
    });
    return await response.json();
  }
}
