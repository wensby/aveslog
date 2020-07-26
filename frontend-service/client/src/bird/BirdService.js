import axios from 'axios';

export default class BirdService {

  async searchBirds(query) {
    return await axios.get(`/api/search?q=${query}`);
  }

  async getBirdStatistics(id) {
    const response = await fetch(`/api/birds/${id}/statistics`);
    if (response.status === 200) {
      return await response.json();
    }
    return null;
  }
}
