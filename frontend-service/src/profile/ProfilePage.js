import React, { useState, useContext, useEffect } from 'react';
import SightingService from '../sighting/SightingService';
import { UserContext } from '../authentication/UserContext';
import { FilterableSightingsList } from '../sighting/FilterableSightingsList';
import { useAccount } from '../account/AccountHooks';

export function ProfilePage({ username }) {
  const [sightings, setSightings] = useState([]);
  const { accessToken } = useContext(UserContext);
  const { account } = useAccount(username);

  useEffect(() => {
    const fetchSightings = async () => {
      const response = await new SightingService().fetchBirderSightings(account.birder.id, accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setSightings(json.items);
      }
    }
    if (account) {
      fetchSightings();
    }
  }, [account]);

  return (
    <div>
      <h1>{username}</h1>
      <FilterableSightingsList sightings={sightings} />
    </div>
  );
};
