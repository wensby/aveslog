export default class BirdService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async queryBirds(query) {
    return await fetch(`${this.apiUrl}/birds?q=${query}`);
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
