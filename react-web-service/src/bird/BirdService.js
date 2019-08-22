export default class BirdService {

  async queryBirds(query) {
    const response = await fetch(`${window._env_.API_URL}/v2/bird?q=${query}`);
    return await response.json();
  }
}
