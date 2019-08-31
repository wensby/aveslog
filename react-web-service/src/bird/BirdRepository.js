import BirdService from "./BirdService";

class BirdRepository {

  constructor() {
    this.birdService = new BirdService();
    this.birdPromisesById = {};
  }

  setUpBirdPromise(birdId) {
    this.birdPromisesById[birdId] = this.birdService.fetchBirdById(birdId)
      .then(response => response.result);
  }

  async getBird(birdId) {
    if (!this.birdPromisesById[birdId]) {
      this.setUpBirdPromise(birdId);
    }
    return await this.birdPromisesById[birdId];
  }
}

const birdRepository = new BirdRepository();
export default birdRepository;
