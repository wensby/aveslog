import React from 'react';
import { SightingCard } from './SightingCard.js';

export const SightingList = ({ sightings }) => {
  return (
    <div>
      {sightings.map(s => <SightingCard key={s.id} sighting={s} />)}
    </div>
  );
};
