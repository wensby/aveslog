import React, { useContext, useState, useEffect } from 'react';
import { Feed } from './Feed';
import SightingService from '../sighting/SightingService';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

const FeedContext = React.createContext();

export const FeedContainer = () => {
  const { getAccessToken, authenticated } = useContext(AuthenticationContext);
  const [sightings, setSightings] = useState([]);

  useEffect(() => {
    const fetchSightings = async () => {
      const accessToken = getAccessToken();
      if (accessToken) {
        const response = await new SightingService().getSightingFeedSightings(accessToken);
        if (response.status === 200) {
          const json = await response.json();
          setSightings(json.items);
        }
      }
    }
    if (authenticated) {
      fetchSightings();
    }
  }, [authenticated, getAccessToken]);

  return (
    <FeedContext.Provider value={{ sightings }}>
      <Feed sightings={sightings} />
    </FeedContext.Provider>
  );
}
