import axios from 'axios';

export default class BirdService {

  async searchBirds(query) {
    return await axios.get(`/api/search?q=${query}`);
  }

  async getBirdStatistics(id) {
    const response = await axios.get(`/api/birds/${id}/statistics`);
    if (response.status === 200) {
      return response.data;
    }
    return null;
  }
}
