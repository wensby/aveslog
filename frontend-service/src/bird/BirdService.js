export default class BirdService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async searchBirds(query) {
    return await fetch(`${this.apiUrl}/search/birds?q=${query}`);
  }

  async getBird(id) {
    const response = await fetch(`${this.apiUrl}/birds/${id}?embed=commonNames`);
    if (response.status === 200) {
      return await response.json();
    }
    return null;
  }

  async getBirdStatistics(id) {
    const response = await fetch(`${this.apiUrl}/birds/${id}/statistics`);
    if (response.status === 200) {
      return await response.json();
    }
    return null;
  }
}
