import React, { useContext, useState, useEffect } from 'react';
import { UserContext } from '../authentication/UserContext';
import personRepository from './PersonRepository';

export function usePerson(personId) {
  const { getAccessToken } = useContext(UserContext);
  const [person, setPerson] = useState(null);

  const resolvePerson = async () => {
    const token = await getAccessToken();
    const person = await personRepository.getPerson(personId, token);
    setPerson(person);
  }

  useEffect(() => {
    resolvePerson();
  }, [personId]);

  return person;
}
