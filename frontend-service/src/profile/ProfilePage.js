import React from 'react';
import { FilterableSightingsList } from '../sighting/FilterableSightingsList';
import { useAccount } from '../account/AccountHooks';
import { LoadingOverlay } from '../loading/LoadingOverlay';
import { useBirderSightings } from '../birder/useBirderSightings';

export function ProfilePage({ username }) {
  const { account } = useAccount(username);
  const { sightings, loading } = useBirderSightings(account ? account.birder : null);

  return (
    <div>
      <h1>{username}</h1>
      {loading && <LoadingOverlay />}
      {!loading && <FilterableSightingsList sightings={sightings} />}
    </div>
  );
};
