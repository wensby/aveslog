export default class BirdService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async queryBirds(query) {
    const response = await fetch(`${this.apiUrl}/v2/bird?q=${query}`);
    return await response.json();
  }

  async getBird(binomialName) {
    const url = `${this.apiUrl}/v2/bird/${binomialName}`;
    const response = await fetch(url);
    return await response.json();
  }
}
