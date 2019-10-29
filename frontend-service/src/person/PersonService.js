class PersonService {

  constructor() {
    this.apiUrl = window._env_.API_URL;
  }

  fetchPerson(personId, accessToken) {
    return fetch(`${window._env_.API_URL}/person/${personId}`, {
      headers: {
        'accessToken': accessToken.jwt,
      },
    })
  }
}
const personService = new PersonService();
export default personService;
