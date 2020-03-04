import React, { useState, useContext, useEffect } from 'react';
import SightingService from '../sighting/SightingService';
import { FilterableSightingsList } from '../sighting/FilterableSightingsList';
import { useAccount } from '../account/AccountHooks';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

export function ProfilePage({ username }) {
  const [sightings, setSightings] = useState([]);
  const { getAccessToken } = useContext(AuthenticationContext);
  const { account } = useAccount(username);

  useEffect(() => {
    const fetchSightings = async () => {
      const accessToken = getAccessToken();
      if (accessToken) {
        const response = await new SightingService().fetchBirderSightings(account.birder.id, accessToken);
        if (response.status === 200) {
          const json = await response.json();
          setSightings(json.items);
        }
      }
    }
    if (account) {
      fetchSightings();
    }
  }, [account, getAccessToken]);

  return (
    <div>
      <h1>{username}</h1>
      <FilterableSightingsList sightings={sightings} />
    </div>
  );
};
