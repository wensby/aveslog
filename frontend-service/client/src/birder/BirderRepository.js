import birderService from './BirderService';

class BirderRepository {

  constructor() {
    this.promiseById = {};
    this.birderById = {};
  }

  async getBirder(birderId) {
    const response = await birderService.fetchBirder(birderId);
    if (response.status === 200) {
      return response.data;
    }
    return null;
  }
}

const repository = new BirderRepository();
export default repository;
