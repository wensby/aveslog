import React, { useState, useEffect, useContext, useCallback } from 'react';
import { UserContext } from '../authentication/UserContext';
import SightingService from './SightingService.js';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

const sightingService = new SightingService();
const SightingContext = React.createContext();

const SightingProvider = props => {
  const { account } = useContext(UserContext);
  const { unauthenticate } = useContext(AuthenticationContext);
  const [sightingsAccount, setSightingsAccount] = useState(null);
  const [sightings, setSightings] = useState([]);

  useEffect(() => {
    if (account !== sightingsAccount) {
      setSightings([]);
    }
    setSightingsAccount(account);
  }, [account, sightingsAccount]);

  const refreshSightings = useCallback(async () => {
    const response = await sightingService.fetchBirderSightings(account.birder.id);
    if (response.status === 200) {
      const fetchedSightings = response.data.items;
      setSightings(prevSightings => {
        if (JSON.stringify(prevSightings) !== JSON.stringify(fetchedSightings)) {
          return fetchedSightings;
        }
        return prevSightings;
      });
    }
    if (response.status === 401) {
      unauthenticate();
    }
  }, [account, unauthenticate]);


  return <SightingContext.Provider value={{ sightings, refreshSightings }}>
    {props.children}
  </SightingContext.Provider>;
}

export { SightingProvider, SightingContext };
