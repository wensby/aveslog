import React, { useState, useContext, useEffect } from 'react';
import SightingService from '../sighting/SightingService';
import { UserContext } from '../authentication/UserContext';
import SightingCard from '../sighting/SightingCard';

export default ({ username }) => {
  const [sightings, setSightings] = useState([]);
  const { getAccessToken } = useContext(UserContext);

  useEffect(() => {
    const fetchSightings = async () => {
      const accessToken = await getAccessToken();
      const response = await new SightingService().fetchSightings(username, accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setSightings(json.items);
      }
    }
    fetchSightings();
  }, [username, getAccessToken]);

  const renderSightings = () => {
    return sightings.map(sighting => <SightingCard sighting={sighting} key={sighting.sightingId} />);
  }

  return (
    <>
      <h1>{username}</h1>
      {renderSightings()}
    </>
  );
};
