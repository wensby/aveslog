import React, { useState, useEffect, useContext } from 'react';
import { UserContext } from '../authentication/UserContext';
import SightingService from './SightingService.js';

const sightingService = new SightingService();
const SightingContext = React.createContext();

const SightingProvider = props => {
  const { account, accessToken, unauthenticate } = useContext(UserContext);
  const [sightingsAccount, setSightingsAccount] = useState(null);
  const [sightings, setSightings] = useState([]);

  useEffect(() => {
    if (account !== sightingsAccount) {
      setSightings([]);
    }
    setSightingsAccount(account);
  }, [account, sightingsAccount]);

  const refreshSightings = async () => {
    const response = await sightingService.fetchBirderSightings(account.birder.id, accessToken);
    if (response.status === 200) {
      const json = await response.json();
      const fetchedSightings = json.items;
      if (JSON.stringify(sightings) !== JSON.stringify(fetchedSightings)) {
        setSightings(fetchedSightings);
      }
    }
    if (response.status === 401) {
      unauthenticate();
    }
  }

  return <SightingContext.Provider value={{
    sightings: sightings,
    refreshSightings: refreshSightings,
  }}>
    {props.children}
  </SightingContext.Provider>;
}

export { SightingProvider, SightingContext };
