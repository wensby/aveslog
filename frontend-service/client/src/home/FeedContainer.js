import React, { useContext, useState, useEffect } from 'react';
import { Feed } from './Feed';
import SightingService from '../sighting/SightingService';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { HomeContext } from 'specific/HomeContext';

const FeedContext = React.createContext();

export const FeedContainer = () => {
  const { getAccessToken, authenticated } = useContext(AuthenticationContext);
  const { homeTrigger } = useContext(HomeContext);
  const [sightings, setSightings] = useState([]);

  useEffect(() => {
    const fetchSightings = async () => {
      const accessToken = await getAccessToken();
      if (accessToken) {
        const response = await fetch('/api/home-feed', {
          headers: {
            'accessToken': accessToken.jwt,
          },
        });
        if (response.status === 200) {
          const json = await response.json();
          setSightings(json.items);
        }
      }
    }
    if (authenticated) {
      fetchSightings();
    }
  }, [authenticated, getAccessToken, homeTrigger]);

  return (
    <FeedContext.Provider value={{ sightings }}>
      <Feed sightings={sightings} />
    </FeedContext.Provider>
  );
}
