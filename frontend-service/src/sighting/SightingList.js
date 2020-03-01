import React from 'react';
import { RevealableSightingCard } from './SightingCard.js';

export const SightingList = ({ sightings }) => {
  return (
    <div>
      {sightings.map(s => <RevealableSightingCard key={s.id} sighting={s} />)}
    </div>
  );
};
