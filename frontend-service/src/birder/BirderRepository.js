import birderService from './BirderService';

class BirderRepository {

  constructor() {
    this.promiseById = {};
    this.birderById = {};
  }

  async getBirder(birderId, token) {
    const response = await birderService.fetchBirder(birderId, token);
    if (response.status === 200) {
      return await response.json();
    }
    return null;
  }
}

const repository = new BirderRepository();
export default repository;
