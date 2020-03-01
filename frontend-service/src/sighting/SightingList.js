import React from 'react';
import { SightingCard, SightingCardPlaceholder } from './SightingCard.js';
import { LazyLoad } from '../LazyLoad.js';

export const SightingList = ({ sightings }) => {
  return (
    <div>
      {sightings.map(s => <LazyLoadedSightingCard key={s.id} sighting={s} />)}
    </div>
  );
};

const LazyLoadedSightingCard = ({ sighting }) => {
  return (
    <LazyLoad offset={1000} placeholder={<SightingCardPlaceholder />}>
      <SightingCard sighting={sighting} />
    </LazyLoad>
  );
};
