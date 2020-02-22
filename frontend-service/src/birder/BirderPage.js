import React, { useContext, useState, useEffect } from 'react';
import { UserContext } from '../authentication/UserContext';
import SightingService from '../sighting/SightingService';
import { FilterableSightingsList } from '../sighting/FilterableSightingsList';

export function BirderPage({ birder }) {
  const { accessToken } = useContext(UserContext);
  const [sightings, setSightings] = useState([]);
  useEffect(() => {
    const fetchSightings = async () => {
      const response = await new SightingService().fetchBirderSightings(birder.id, accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setSightings(json.items);
      }
    }
    fetchSightings();
  }, [birder]);
  return (
    <div>
      <h1>{birder.name}</h1>
      <FilterableSightingsList sightings={sightings} />
    </div>
  );
}
