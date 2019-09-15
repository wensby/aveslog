export default class SightingService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async fetchSightings(username, authToken) {
    return await fetch(`${this.apiUrl}/v2/profile/${username}/sighting`, {
      'headers': {
        'authToken': authToken,
      },
    });
  }

  async fetchSighting(authToken, sightingId) {
    const url = `${this.apiUrl}/v2/sighting/${sightingId}`;
    const response = await fetch(url, {
      'headers': {
        'authToken': authToken,
      },
    });
    return await response.json();
  }

  async postSighting(authToken, personId, binomialName, date, time) {
    const body = {
      'person': { 'id': personId },
      'bird': { 'binomialName': binomialName },
      'date': date,
    };
    if (time) {
      body['time'] = time;
    }
    const response = await fetch(
      `${this.apiUrl}/v2/sighting`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'authToken': authToken,
      },
      body: JSON.stringify(body),
    });
    return await response.json();
  }

  async deleteSighting(authToken, sightingId) {
    const response = await fetch(`${this.apiUrl}/v2/sighting/${sightingId}`, {
      method: 'DELETE',
      headers: {
        'authToken': authToken,
      },
    });
    return response.status == 204;
  }
}
