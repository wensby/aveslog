import personService from './PersonService';

class PersonRepository {
  
  constructor() {
    this.promiseById = {};
    this.personById = {};
  }

  async getPerson(personId, token) {
    this.setUpPersonFetch(personId, token);
    await this.resolveOngoingFetch(personId);
    delete this.promiseById[personId];
    return this.personById[personId];
  }

  setUpPersonFetch(personId, token) {
    if (personId in this.promiseById) {
      console.log('person fetch already in progress');
    }
    else {
      this.promiseById[personId] = personService.fetchPerson(personId, token);
    }
  }

  async resolveOngoingFetch(personId) {
    const response = await this.promiseById[personId];
    if (response.status === 200) {
      this.personById[personId] = await response.clone().json();
    }
  }
}

const repository = new PersonRepository();
export default repository;
