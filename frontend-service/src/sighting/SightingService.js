export default class SightingService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  async fetchSightings(username, accessToken) {
    return await fetch(`${this.apiUrl}/profile/${username}/sighting`, {
      'headers': {
        'accessToken': accessToken,
      },
    });
  }

  async fetchSighting(accessToken, sightingId) {
    const url = `${this.apiUrl}/sighting/${sightingId}`;
    const response = await fetch(url, {
      'headers': {
        'accessToken': accessToken,
      },
    });
    return await response.json();
  }

  async postSighting(accessToken, personId, binomialName, date, time) {
    const body = {
      'person': { 'id': personId },
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
        'accessToken': accessToken,
      },
      body: JSON.stringify(body),
    });
    return response;
  }

  async deleteSighting(accessToken, sightingId) {
    const response = await fetch(`${this.apiUrl}/sighting/${sightingId}`, {
      method: 'DELETE',
      headers: {
        'accessToken': accessToken,
      },
    });
    return response.status == 204;
  }
}
