import React, { useState, useEffect, useContext } from 'react';
import SightingList from './SightingList.js';
import SightingService from './SightingService.js';
import { AuthenticationContext } from '../authentication/AuthenticationContext.js';

export default () => {
  const [sightings, setSightings] = useState([]);
  const { account, token, unauthenticate } = useContext(AuthenticationContext);
  const sightingService = new SightingService();

  const fetchSightings = async () => {
    const username = account.username;
    const response = await sightingService.fetchSightings(username, token);
    if (response.status == 401) {
      unauthenticate();
    }
    else {
      const content = await response.json();
      if (content.status == 'success') {
        setSightings(content.result.sightings);
      }
    }
  }

  useEffect(() => {
    fetchSightings();
  }, []);

  return <SightingList sightings={sightings} />;
}
