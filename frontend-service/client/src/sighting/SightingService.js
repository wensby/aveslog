import axios from 'axios';

export default class SightingService {

  async getSightingFeedSightings() {
    return await axios.get('/api/sightings?limit=10');
  }

  async fetchBirderSightings(birderId) {
    return await axios.get(`/api/birders/${birderId}/sightings`);
  }

  async fetchSightingByLocation(location) {
    const response = await axios.get(`/api${location}`);
    return response.data;
  }

  async fetchSighting(sightingId) {
    return await axios.get(`/api/sightings/${sightingId}`);
  }

  async postSighting(birderId, binomialName, date, time, location) {
    const body = {
      'birder': { 'id': birderId },
      'bird': { 'binomialName': binomialName },
      'date': date,
    };
    if (time) {
      body['time'] = time;
    }
    if (location) {
      body['position'] = {
        'lat': location[0],
        'lon': location[1]
      }
    }
    const response = await axios.post('/api/sightings', body);
    return response;
  }

  async deleteSighting(sightingId) {
    const response = await axios.delete(`/api/sightings/${sightingId}`);
    return response.status === 204;
  }
}
