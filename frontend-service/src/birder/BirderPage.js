import React, { useContext, useState, useEffect } from 'react';
import SightingService from '../sighting/SightingService';
import { FilterableSightingsList } from '../sighting/FilterableSightingsList';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

export function BirderPage({ birder }) {
  const { getAccessToken } = useContext(AuthenticationContext);
  const [sightings, setSightings] = useState([]);
  useEffect(() => {
    const fetchSightings = async () => {
      const accessToken = getAccessToken();
      if (accessToken) {
        const response = await new SightingService().fetchBirderSightings(birder.id, accessToken);
        if (response.status === 200) {
          const json = await response.json();
          setSightings(json.items);
        }
      }
    }
    fetchSightings();
  }, [birder, getAccessToken]);
  return (
    <div>
      <h1>{birder.name}</h1>
      <FilterableSightingsList sightings={sightings} />
    </div>
  );
}
