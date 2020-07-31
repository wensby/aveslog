import { useState, useEffect } from 'react';
import SightingService from '../sighting/SightingService';

export const useBirderSightings = birder => {
  const [sightingsBirder, setSightingsBirder] = useState();
  const [sightings, setSightings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSightings = async () => {
      setLoading(true);
      const response = await new SightingService().fetchBirderSightings(birder.id);
      if (response.status === 200) {
        setSightings(response.data.items);
        setSightingsBirder(birder);
      }
      setLoading(false);
    }
    if (birder) {
      if (!sightingsBirder || sightingsBirder.id !== birder.id) {
        setSightings([]);
        fetchSightings();
      }
    }
    else {
      setSightings([]);
    }
  }, [birder, sightingsBirder]);

  return { sightings, loading, error };
};
