import React from 'react';
import { RevealableSightingListItem } from './RevealableSightingListItem';

export const SightingsList = ({ sightings }) => {
  return (
    <div>
      {sightings.map(s => <RevealableSightingListItem key={s.id} sighting={s} />)}
    </div>
  );
};
