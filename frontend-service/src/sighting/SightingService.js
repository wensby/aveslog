export default class SightingService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async getSightingFeedSightings(accessToken) {
    return await fetch(`${this.apiUrl}/sighting?limit=10`, {
      'headers': {
        'accessToken': accessToken.jwt,
      },
    });
  }

  async fetchSightings(username, accessToken) {
    return await fetch(`${this.apiUrl}/profile/${username}/sighting`, {
      'headers': {
        'accessToken': accessToken.jwt,
      },
    });
  }

  async fetchBirderSightings(birderId, accessToken) {
    return await fetch(`${this.apiUrl}/birders/${birderId}/sightings`, {
      'headers': {
        'accessToken': accessToken.jwt,
      },
    });
  }

  async fetchSightingByLocation(accessToken, location) {
    const url = `${this.apiUrl}${location}`;
    const response = await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt,
      },
    });
    return await response.json();
  }

  async fetchSighting(accessToken, sightingId) {
    const url = `${this.apiUrl}/sighting/${sightingId}`;
    return await fetch(url, {
      'headers': {
        'accessToken': accessToken.jwt,
      },
    });
  }

  async postSighting(accessToken, birderId, binomialName, date, time) {
    const body = {
      'birder': { 'id': birderId },
      'bird': { 'binomialName': binomialName },
      'date': date,
    };
    if (time) {
      body['time'] = time;
    }
    const response = await fetch(
      `${this.apiUrl}/sighting`, {
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
    const response = await fetch(`${this.apiUrl}/sighting/${sightingId}`, {
      method: 'DELETE',
      headers: {
        'accessToken': accessToken.jwt,
      },
    });
    return response.status === 204;
  }
}
