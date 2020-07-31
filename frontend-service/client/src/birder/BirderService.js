import axios from 'axios';

class BirderService {

  fetchBirder(birderId) {
    return axios.get(`/api/birders/${birderId}`)
  }
}
const birderService = new BirderService();
export default birderService;
