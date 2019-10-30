import birderService from './BirderService';

class BirderRepository {

  constructor() {
    this.promiseById = {};
    this.birderById = {};
  }

  async getBirder(birderId, token) {
    this.setUpBirderFetch(birderId, token);
    await this.resolveOngoingFetch(birderId);
    delete this.promiseById[birderId];
    return this.birderById[birderId];
  }

  setUpBirderFetch(birderId, token) {
    if (birderId in this.promiseById) {
      console.log('birder fetch already in progress');
    }
    else {
      this.promiseById[birderId] = birderService.fetchBirder(birderId, token);
    }
  }

  async resolveOngoingFetch(birderId) {
    const response = await this.promiseById[birderId];
    if (response.status === 200) {
      this.birderById[birderId] = await response.clone().json();
    }
  }
}

const repository = new BirderRepository();
export default repository;
