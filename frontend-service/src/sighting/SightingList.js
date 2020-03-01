import React from 'react';
import { SightingCard } from './SightingCard.js';

export const SightingList = ({ sightings }) => {
  return (
    <div>
      {sightings.map(s => <LazyLoadedSightingCard key={s.id} sighting={s} />)}
    </div>
  );
};

const LazyLoadedSightingCard = ({ sighting }) => {
  return <SightingCard sighting={sighting} />;
};
