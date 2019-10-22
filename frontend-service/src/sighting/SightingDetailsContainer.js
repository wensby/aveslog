import React, { useState, useEffect, useContext } from 'react';
import SightingDetails from './SightingDetails';
import { UserContext }  from '../authentication/UserContext';
import SightingService from './SightingService';

export default function SightingDetailsContainer(props) {
  const sightingId = props.match.params.sightingId;
  const [sighting, setSighting] = useState(null);
  const { getAccessToken } = useContext(UserContext);
  const sightingService = new SightingService();

  useEffect(() => {
    const resolveSighting = async () => {
      const accessToken = await getAccessToken();
      const response = await sightingService.fetchSighting(accessToken, sightingId);
      if (response.status === 'success') {
        const sighting = response.result;
        setSighting(sighting);
      }
    }
    resolveSighting();
  }, [sightingId]);

  if (!sighting) {
    return null;
  }
  return <SightingDetails sighting={sighting}/>;
}
