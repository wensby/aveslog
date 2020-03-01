import React from 'react';
import { SightingCard, SightingCardPlaceholder } from './SightingCard.js';
import { LazyLoad } from '../LazyLoad.js';

export const SightingList = ({ sightings }) => {
  return (
    <div className='text-break'>
      {sightings.map(s => <LazyLoadedSightingCard sighting={s} />)}
    </div>
  );
};

const LazyLoadedSightingCard = ({ sighting }) => {
  return (
    <LazyLoad offset={1000} key={sighting.id} placeholder={<SightingCardPlaceholder />}>
      <SightingCard sighting={sighting} />
    </LazyLoad>
  );
}
