import React, { useState, useContext, useEffect } from 'react';
import SightingService from '../sighting/SightingService';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

export const useBirderSightings = birder => {
  const { getAccessToken } = useContext(AuthenticationContext);
  const [sightingsBirder, setSightingsBirder] = useState();
  const [sightings, setSightings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSightings = async () => {
      setLoading(true);
      const accessToken = await getAccessToken();
      if (accessToken) {
        const response = await new SightingService().fetchBirderSightings(birder.id, accessToken);
        if (response.status === 200) {
          const json = await response.json();
          setSightings(json.items);
          setSightingsBirder(birder);
        }
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
  }, [birder, sightingsBirder, getAccessToken]);

  return { sightings, loading, error };
};
