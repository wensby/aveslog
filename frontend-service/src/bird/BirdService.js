export default class BirdService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async queryBirds(query) {
    const response = await fetch(`${this.apiUrl}/bird?q=${query}`);
    return await response.json();
  }

  async getBird(binomialName) {
    const response = await fetch(`${this.apiUrl}/bird/${binomialName}`);
    return await response.json();
  }

  async fetchBirdById(id) {
    const response = await fetch(`${this.apiUrl}/bird/${id}`);
    return await response.json();
  }
}
