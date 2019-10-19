import React, { useEffect, useContext } from 'react';
import SightingList from './SightingList.js';
import { SightingContext } from './SightingContext';

export default function SightingsPage() {
  const { sightings, refreshSightings } = useContext(SightingContext);

  useEffect(() => {
    refreshSightings();
  }, []);

  return <SightingList sightings={sightings} />;
}
