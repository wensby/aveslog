import BirdService from "./BirdService";

class BirdRepository {

  constructor() {
    this.birdService = new BirdService();
  }

  async getBird(birdId) {
    return await this.birdService.getBird(birdId);
  }

  async getBirdStatistics(birdId) {
    return await this.birdService.getBirdStatistics(birdId);
  }
}

const birdRepository = new BirdRepository();
export default birdRepository;
