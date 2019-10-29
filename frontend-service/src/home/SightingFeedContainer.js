import React, { useContext, useState, useEffect } from 'react';
import SightingFeed from './SightingFeed';
import { UserContext } from '../authentication/UserContext';
import SightingService from '../sighting/SightingService';

export default function SightingFeedContainer({ }) {
  const { getAccessToken } = useContext(UserContext);
  const [sightings, setSightings] = useState([]);
  useEffect(() => {
    const fetchSightings = async () => {
      const accessToken = await getAccessToken();
      const response = await new SightingService().getSightingFeedSightings(accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setSightings(json.items);
      }
    }
    fetchSightings();
  }, []);
  return <SightingFeed sightings={sightings} />;
}
