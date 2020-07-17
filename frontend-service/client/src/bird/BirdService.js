export default class BirdService {

  async searchBirds(query, accessToken) {
    const headers = {};
    if (accessToken) {
      headers['accessToken'] = accessToken.jwt;
    }
    return await fetch(`/api/search/birds?q=${query}&embed=stats`, {
      headers: headers
    });
  }

  async getBirdStatistics(id) {
    const response = await fetch(`/api/birds/${id}/statistics`);
    if (response.status === 200) {
      return await response.json();
    }
    return null;
  }
}
