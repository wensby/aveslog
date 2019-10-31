export default class BirdService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async searchBirds(query) {
    return await fetch(`${this.apiUrl}/search/birds?q=${query}`);
  }

  async getBird(binomialName) {
    const response = await fetch(`${this.apiUrl}/birds/${binomialName}`);
    return await response.json();
  }

  async fetchBirdById(id) {
    const response = await fetch(`${this.apiUrl}/birds/${id}`);
    return await response.json();
  }
}
