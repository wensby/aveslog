import React, { useEffect, useContext } from 'react';
import SightingList from './SightingList.js';
import { SightingContext } from './SightingContext';
import { SightingsStats } from './SightingsStats';

export default function SightingsPage() {
  const { sightings, refreshSightings } = useContext(SightingContext);

  useEffect(() => {
    refreshSightings();
  }, []);

  return (
    <>
      <SightingsStats sightings={sightings} />
      <SightingList sightings={sightings} />
    </>
  );
}
