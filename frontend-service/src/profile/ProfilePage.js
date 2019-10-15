import React, { useState, useContext, useEffect } from 'react';
import SightingService from '../sighting/SightingService';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import SightingItem from '../sighting/SightingItem';

export default ({ username }) => {
  const [sightings, setSightings] = useState([]);
  const { getAccessToken } = useContext(AuthenticationContext);

  useEffect(() => {
    const fetchSightings = async () => {
      const accessToken = await getAccessToken();
      const response = await new SightingService().fetchSightings(username, accessToken);
      if (response.status === 401) {

      }
      else {
        const content = await response.json();
        if (content.status === 'success') {
          setSightings(content.result.sightings);
        }
      }
    }
    fetchSightings();
  }, [username, getAccessToken]);

  const renderSightings = () => {
    return sightings.map(sighting => <SightingItem sighting={sighting} />);
  }

  return (
    <>
      <h1>{username}</h1>
      {renderSightings()}
    </>
  );
};
