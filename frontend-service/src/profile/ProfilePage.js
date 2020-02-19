import React, { useState, useContext, useEffect } from 'react';
import SightingService from '../sighting/SightingService';
import { UserContext } from '../authentication/UserContext';
import AccountService from '../account/AccountService';
import { FilterableSightingsList } from '../sighting/FilterableSightingsList';

export function ProfilePage({ username }) {
  const [sightings, setSightings] = useState([]);
  const { accessToken } = useContext(UserContext);
  const [account, setAccount] = useState(null);

  useEffect(() => {
    const fetchAccount = async () => {
      const response = await new AccountService().fetchAccount(accessToken, username);
      if (response.status === 200) {
        setAccount(await response.json());
      }
    };
    fetchAccount();
  }, [username, accessToken])

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
  }, [account, accessToken]);

  return (
    <div>
      <h1>{username}</h1>
      <FilterableSightingsList sightings={sightings} />
    </div>
  );
};
