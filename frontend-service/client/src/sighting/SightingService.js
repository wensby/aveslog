import axios from 'axios';

export default class SightingService {

  async getSightingFeedSightings(accessToken) {
    return await fetch('/api/sightings?limit=10', {
      'headers': {
        'accessToken': accessToken.jwt,
      },
    });
  }

  async fetchBirderSightings(birderId) {
    return await axios.get(`/api/birders/${birderId}/sightings`);
  }

  async fetchSightingByLocation(accessToken, location) {
    const url = `/api${location}`;
    const response = await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt,
      },
    });
    return await response.json();
  }

  async fetchSighting(accessToken, sightingId) {
    const url = `/api/sightings/${sightingId}`;
    return await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt,
      },
    });
  }

  async postSighting(accessToken, birderId, binomialName, date, time, location) {
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
    const response = await fetch('/api/sightings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'accessToken': accessToken.jwt,
      },
      body: JSON.stringify(body),
    });
    return response;
  }

  async deleteSighting(accessToken, sightingId) {
    const response = await fetch(`/api/sightings/${sightingId}`, {
      method: 'DELETE',
      headers: {
        'accessToken': accessToken.jwt,
      },
    });
    return response.status === 204;
  }
}
