import React, { useState, useEffect, useContext } from 'react';
import SightingList from './SightingList.js';
import { SightingContext } from './SightingContext';

export default () => {
  const { sightings, refreshSightings } = useContext(SightingContext);

  useEffect(() => {
    refreshSightings();
  }, []);

  return <SightingList sightings={sightings} />;
}
