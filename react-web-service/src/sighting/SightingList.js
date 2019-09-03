import React, { useState, useEffect, useContext } from 'react';
import SightingService from './SightingService.js';
import { AuthenticationContext } from '../authentication/AuthenticationContext.js';
import SightingItem from './SightingItem';

export default () => {
  const [sightings, setSightings] = useState([]);
  const { account, token } = useContext(AuthenticationContext);
  const sightingService = new SightingService();

  const fetchSightings = async () => {
    const username = account.username;
    const response = await sightingService.fetchSightings(username, token);
    if (response.status == 'success') {
      setSightings(response.result.sightings);
    }
  }

  useEffect(() => {
    fetchSightings();
  }, []);

  const renderSightingItem = sighting => {
    return <SightingItem sighting={sighting} key={sighting.sightingId} />;
  };

  return (
    <div className="text-break">
      {sightings.map(renderSightingItem)}
    </div>
  );
}
