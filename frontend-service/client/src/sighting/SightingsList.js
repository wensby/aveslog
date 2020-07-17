import React from 'react';
import { RevealableSightingListItem } from './RevealableSightingListItem';

export const SightingsList = ({ sightings }) => {
  return (
    <div>
      {sightings.map((s, i) => <RevealableSightingListItem key={i} sighting={s} />)}
    </div>
  );
};
