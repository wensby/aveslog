import React from 'react';
import { RevealingSightingCard } from './SightingCard.js';

export const SightingList = ({ sightings }) => {
  return (
    <div>
      {sightings.map(s => <RevealingSightingCard key={s.id} sighting={s} />)}
    </div>
  );
};
