import React, { useContext, useState, useEffect } from 'react';
import { SightingFeed } from './SightingFeed';
import { UserContext } from '../authentication/UserContext';
import SightingService from '../sighting/SightingService';

const FeedContext = React.createContext();

export const SightingFeedContainer = () => {
  const { accessToken, authenticated } = useContext(UserContext);
  const [sightings, setSightings] = useState([]);

  useEffect(() => {
    const fetchSightings = async () => {
      const response = await new SightingService().getSightingFeedSightings(accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setSightings(json.items);
      }
    }
    if (authenticated) {
      fetchSightings();
    }
  }, [authenticated]);

  return (
    <FeedContext.Provider value={{sightings}}>
      <SightingFeed sightings={sightings} />
    </FeedContext.Provider>
  );
}
